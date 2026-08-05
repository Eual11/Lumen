from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import os

import numpy as np
import SimpleITK as sitk
from vtkmodules.vtkCommonCore import VTK_FLOAT, VTK_INT, VTK_SHORT
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkCommonExecutionModel import vtkTrivialProducer
from vtkmodules.util import numpy_support


@dataclass
class DicomSeries:
    """One acquisition inside a DICOM folder."""
    uid: str
    files: List[str] = field(default_factory=list)
    description: str = ""
    modality: str = ""
    patient_name: str = ""
    study_description: str = ""

    @property
    def num_slices(self) -> int:
        return len(self.files)

    def label(self) -> str:
        desc = self.description or "<no description>"
        return f"{desc} ({self.modality}, {self.num_slices} slices)"


# DICOM tags read for display. GDCM exposes them lowercase-hex, group|element.
_TAG_PATIENT_NAME = "0010|0010"
_TAG_MODALITY = "0008|0060"
_TAG_SERIES_DESC = "0008|103e"
_TAG_STUDY_DESC = "0008|1030"


class DicomLoader:
    """Loads DICOM series into VTK.

    Uses SimpleITK/GDCM rather than vtkDICOMImageReader because the latter
    supports neither compressed transfer syntaxes (JPEG Lossless, JPEG2000,
    RLE) nor files written without the 128-byte preamble and 'DICM' magic.
    Both are common in PACS exports and each one silently yields an empty
    volume.
    """

    def __init__(self) -> None:
        self.producer: Optional[vtkTrivialProducer] = None
        self.image: Optional[vtkImageData] = None
        self.ouput_port = None

        self.series: List[DicomSeries] = []
        self.current_series: Optional[DicomSeries] = None

    def _cleanup(self):
        self.producer = None
        self.image = None
        self.ouput_port = None
        self.current_series = None

    # ------------------------------------------------------------------
    # discovery
    # ------------------------------------------------------------------
    def scan_series(self, path: str) -> List[DicomSeries]:
        """Enumerate every series in a directory, largest first.

        A folder pulled off a PACS routinely holds several acquisitions with
        different matrix sizes and spacings, so they cannot be stacked into one
        volume -- the caller has to pick one.
        """
        self.series = []

        if not path or not os.path.isdir(path):
            return self.series

        reader = sitk.ImageSeriesReader()
        try:
            uids = reader.GetGDCMSeriesIDs(path)
        except Exception as exc:
            print(f"[DicomLoader] could not scan '{path}': {exc}")
            return self.series

        for uid in uids:
            try:
                files = list(reader.GetGDCMSeriesFileNames(path, uid))
            except Exception as exc:
                print(f"[DicomLoader] skipping series {uid}: {exc}")
                continue
            if not files:
                continue

            series = DicomSeries(uid=uid, files=files)
            self._read_series_metadata(series)
            self.series.append(series)

        self.series.sort(key=lambda s: s.num_slices, reverse=True)
        return self.series

    def _read_series_metadata(self, series: DicomSeries):
        """Pull display metadata from the first slice of a series."""
        file_reader = sitk.ImageFileReader()
        file_reader.SetFileName(series.files[0])
        file_reader.LoadPrivateTagsOff()
        try:
            file_reader.ReadImageInformation()
        except Exception:
            return

        def tag(key: str) -> str:
            try:
                return file_reader.GetMetaData(key).strip()
            except Exception:
                return ""

        series.description = tag(_TAG_SERIES_DESC)
        series.modality = tag(_TAG_MODALITY)
        series.patient_name = tag(_TAG_PATIENT_NAME).replace("^", " ").strip()
        series.study_description = tag(_TAG_STUDY_DESC)

    # ------------------------------------------------------------------
    # loading
    # ------------------------------------------------------------------
    def load_imge(self, path, series_uid: Optional[str] = None) -> bool:
        """Load a DICOM directory (or single file) into the VTK pipeline.

        When the directory holds several series and none is named, the one with
        the most slices wins. Returns True when a volume was produced.
        """
        self._cleanup()

        if not path or not os.path.exists(path):
            print(f"[DicomLoader] path does not exist: {path}")
            return False

        try:
            if os.path.isdir(path):
                sitk_image = self._read_directory(path, series_uid)
            else:
                sitk_image = self._read_single_file(path)
        except Exception as exc:
            print(f"[DicomLoader] failed to read '{path}': {exc}")
            return False

        if sitk_image is None:
            return False

        try:
            self.image = self._sitk_to_vtk(sitk_image)
        except Exception as exc:
            print(f"[DicomLoader] failed to convert image to VTK: {exc}")
            self._cleanup()
            return False

        self.producer = vtkTrivialProducer()
        self.producer.SetOutput(self.image)
        self.producer.Update()
        self.ouput_port = self.producer.GetOutputPort()
        return True

    def _read_directory(self, path: str, series_uid: Optional[str]):
        if not self.series or (series_uid and series_uid not in {s.uid for s in self.series}):
            self.scan_series(path)

        if not self.series:
            raise RuntimeError("no DICOM series found in directory")

        selected = None
        if series_uid:
            selected = next((s for s in self.series if s.uid == series_uid), None)
        if selected is None:
            # scan_series sorts by slice count, so the first is the largest.
            selected = self.series[0]

        reader = sitk.ImageSeriesReader()
        reader.SetFileNames(selected.files)
        image = reader.Execute()

        self.current_series = selected
        return image

    def _read_single_file(self, path: str):
        reader = sitk.ImageFileReader()
        reader.SetFileName(path)
        image = reader.Execute()

        series = DicomSeries(uid="", files=[path])
        self._read_series_metadata(series)
        self.series = [series]
        self.current_series = series
        return image

    def _sitk_to_vtk(self, sitk_image) -> vtkImageData:
        """Convert a SimpleITK volume to vtkImageData, preserving geometry.

        GDCM applies RescaleSlope/Intercept, which can promote the array to
        float even though the values are integral, so narrow it back to the
        smallest integer type that fits. Downstream thresholding and marching
        cubes both assume integral scalars.
        """
        arr = sitk.GetArrayFromImage(sitk_image)  # (z, y, x)

        if arr.ndim == 4:
            # RGB / multi-component: keep components as the trailing axis.
            raise RuntimeError("multi-component DICOM images are not supported")

        vtk_type = VTK_SHORT
        if np.issubdtype(arr.dtype, np.floating):
            rounded = np.rint(arr)
            if np.allclose(arr, rounded, atol=1e-4):
                arr = rounded
            else:
                vtk_type = VTK_FLOAT

        if vtk_type != VTK_FLOAT:
            lo, hi = float(arr.min()), float(arr.max())
            if lo >= np.iinfo(np.int16).min and hi <= np.iinfo(np.int16).max:
                arr = arr.astype(np.int16)
                vtk_type = VTK_SHORT
            elif lo >= np.iinfo(np.int32).min and hi <= np.iinfo(np.int32).max:
                arr = arr.astype(np.int32)
                vtk_type = VTK_INT
            else:
                arr = arr.astype(np.float32)
                vtk_type = VTK_FLOAT
        else:
            arr = arr.astype(np.float32)

        # deep=True: the ravel() buffer is temporary and VTK must own the copy.
        vtk_array = numpy_support.numpy_to_vtk(
            arr.ravel(order="C"), deep=True, array_type=vtk_type
        )

        image = vtkImageData()
        image.SetDimensions(*sitk_image.GetSize())          # (x, y, z)
        image.SetSpacing(*sitk_image.GetSpacing())
        image.SetOrigin(*sitk_image.GetOrigin())
        image.GetPointData().SetScalars(vtk_array)
        image.Modified()
        return image

    # ------------------------------------------------------------------
    # queries
    # ------------------------------------------------------------------
    def get_image_dimensions(self) -> Tuple[int, int, int, int, int, int]:
        if self.image:
            return self.image.GetExtent()
        return 0, 0, 0, 0, 0, 0

    def get_num_slices(self) -> int:
        if self.image:
            extent = self.image.GetExtent()
            return extent[5] - extent[4] + 1
        return 0

    def get_scalar_range(self) -> Tuple[float, float]:
        if self.image:
            return self.image.GetScalarRange()
        return 0.0, 0.0

    def get_medical_property(self) -> List[str]:
        if not self.current_series:
            return []

        parts = []
        if self.current_series.patient_name:
            parts.append(self.current_series.patient_name)
        if self.current_series.study_description:
            parts.append(self.current_series.study_description)
        if self.current_series.description:
            parts.append(self.current_series.description)
        if self.current_series.modality:
            parts.append(self.current_series.modality)
        return parts

    def get_series(self) -> List[DicomSeries]:
        return self.series

    def get_output_port(self):
        return self.ouput_port
