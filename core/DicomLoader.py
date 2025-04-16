from typing import List, Tuple
from vtk import vtkDICOMImageReader

from PySide6.QtWidgets import QVBoxLayout, QWidget, QMessageBox
import os
class DicomLoader:
    def __init__(self) -> None:
        self.reader = vtkDICOMImageReader()
        self.ouput_port = None

    def _cleanup(self):
        if self.reader:
            self.raeder = None

    def load_imge(self, path):
        self._cleanup()
        self.reader = vtkDICOMImageReader()

        if(not os.path.exists(path)):
            return

        if(os.path.isdir(path)):
            self.reader.SetDirectoryName(path)
        else:
            return

        try:
            self.reader.Update()
            self.ouput_port = self.reader.GetOutputPort()
        except:
            print("Failed to load ")
    def get_image_dimensions(self)->Tuple[int, int, int, int, int, int]:
        if(self.reader):
            return self.reader.GetDataExtent()
        return 0,0,0,0,0,0
    def get_num_slices(self)->int:
        if(self.reader):
            return self.reader.GetDataExtent()[-1]
        return 0
    def get_medical_property(self)->List[str]:
        if(self.reader):
            return [str(self.reader.GetPatientName())] 
        return []

    def get_output_port(self):
        return self.ouput_port







