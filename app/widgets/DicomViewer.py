from typing import List, Optional,Tuple
from PySide6.QtWidgets import QVBoxLayout, QWidget, QMessageBox
from typing import TypedDict
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

from utils.utils import numpyArrToVtkImageData

from .ImageViewerUI import Ui_ImageViewerUI
from core.Segment import Segment

class SegmentActorInfo(TypedDict):
    actor: vtk.vtkImageSlice
    mapper: vtk.vtkImageResliceMapper
    lut: vtk.vtkLookupTable

class DicomViewer(QWidget):
    def __init__(self, source: Optional[vtk.vtkAlgorithmOutput] = None, parent=None):
        super().__init__(parent)

        self.ui = Ui_ImageViewerUI()
        self.ui.setupUi(self)

        self.vtkInteractor = QVTKRenderWindowInteractor(self.ui.vtkParent)
        layout = QVBoxLayout()
        layout.addWidget(self.vtkInteractor)
        self.ui.vtkParent.setLayout(layout)

        self.renderer = vtk.vtkRenderer()
        self.render_window = self.vtkInteractor.GetRenderWindow()
        self.render_window.AddRenderer(self.renderer)

        self.mapper = vtk.vtkImageResliceMapper()
        self.mapper.SliceFacesCameraOff()
        self.mapper.SliceAtFocalPointOff()
        self.slice_actor = vtk.vtkImageSlice()
        self.slice_actor.SetMapper(self.mapper)
        self.renderer.AddViewProp(self.slice_actor)

        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.vtkInteractor.SetInteractorStyle(vtk.vtkInteractorStyleImage())

        self.ui.sliceSlider.valueChanged.connect(self.setSliceIdx)

        self.spacing = (1.0, 1.0, 1.0)
        self.extent = (0, 0, 0, 0, 0, 0)
        self.origin = (0.0, 0.0, 0.0)


        self.segment_overlay_masks: dict[Segment, SegmentActorInfo] = {}

        self.updateSource(source)

    def setPatientDat(self, arr: List[str]):
        self.ui.imageInfo.setText(" ".join(arr))

    def renderImage(self):
        self.render_window.Render()

    def setSliceIdx(self, idx: int):
        if self.mapper:
            z = self.origin[2] + idx * self.spacing[2]

            plane = vtk.vtkPlane()
            plane.SetOrigin(self.origin[0], self.origin[1], z)
            plane.SetNormal(0, 0, 1)

            self.mapper.SetSlicePlane(plane)
            for value in self.segment_overlay_masks.values():
                mapper = value['mapper']
                mapper.SetSlicePlane(plane)
                mapper.Update()
            self.ui.sliceIdxLabel.setText(f"Slice: {idx + 1}/{self.ui.sliceSlider.maximum() + 1}")
            self.renderImage()

    def cleanup(self):
        self.vtkInteractor.GetRenderWindow().Finalize()

    def updateSource(self, source: Optional[vtk.vtkAlgorithmOutput]):
        self.source = source
        if source:
            self.mapper.SetInputConnection(source)
            source.GetProducer().Update()
            image_data = source.GetProducer().GetOutput()

            self.spacing = image_data.GetSpacing()
            self.origin = image_data.GetOrigin()
            self.extent = image_data.GetExtent()

            zmin, zmax = self.extent[4], self.extent[5]


            self.ui.sliceSlider.setMinimum(zmin)
            self.ui.sliceSlider.setMaximum(zmax)
            self.ui.sliceSlider.setValue(zmin)
            self.setSliceIdx(zmin)

            self.renderer.ResetCamera()
            self.renderImage()
        else:
            self.mapper.SetInputConnection(None)
    def add_segment_overlay(self,segment:Segment):
        mapper = vtk.vtkImageResliceMapper()
        img_data = numpyArrToVtkImageData(segment.mask, self.spacing, vtk.VTK_CHAR)
        mapper.SetInputData(img_data)

        mapper.SliceFacesCameraOff()
        mapper.SliceAtFocalPointOff()

        lut = vtk.vtkLookupTable()
        lut.SetNumberOfTableValues(2)
        lut.SetRange(0,1)
        lut.Build()
        lut.SetTableValue(0,0.0,0.0,0.0,0.0)
        cols =[c/255.0 for c in segment.color] 
        lut.SetTableValue(1,cols[0],cols[1], cols[2],0.5)

        actor = vtk.vtkImageSlice()
        actor.SetMapper(mapper)
        actor.GetProperty().SetLookupTable(lut)
        actor.GetProperty().UseLookupTableScalarRangeOn()

        self.segment_overlay_masks[segment] = {
            "actor": actor,
            "mapper": mapper,
            "lut":lut
        }

        self.renderer.AddViewProp(actor)
        self.render_window.Render()




    def remove_segment_overlay(self,segment:Segment):
        info = self.segment_overlay_masks[segment]
        self.renderer.RemoveActor(info['actor'])
        del self.segment_overlay_masks[segment]

        self.render_window.Render()
    def set_segment_visibility(self, segment:Segment, value):
        segment_info = self.segment_overlay_masks[segment]
        segment_info['actor'].SetVisibility(value)

        self.render_window.Render()
    def set_segment_color(self, segment:Segment, value:Tuple[int,int,int]):
        segment_info = self.segment_overlay_masks[segment]
        lut = segment_info['lut']
        cols = [c/255.0 for c in value]
        lut.SetTableValue(1, cols[0], cols[1], cols[2],0.5)
        lut.Modified()
        self.render_window.Render()

    def showErrorMessage(self, title, desc):
        QMessageBox.critical(self, title, desc)

