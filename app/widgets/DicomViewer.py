from typing import List, Optional
from PySide6.QtWidgets import QVBoxLayout, QWidget, QMessageBox
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import os

from core import DicomLoader

from .ImageViewerUI import Ui_ImageViewerUI


class DicomViewer(QWidget):
    def __init__(self,source:Optional[vtk.vtkAlgorithmOutput]=None,parent=None):
        super().__init__(parent)

        self.ui =Ui_ImageViewerUI()
        self.ui.setupUi(self)
        self.input_data_extent = 0,0,0,0,0,0

        self.viewer = vtk.vtkImageViewer2()
        self.vtkInteractor = QVTKRenderWindowInteractor(self.ui.vtkParent)

        layout = QVBoxLayout()
        layout.addWidget(self.vtkInteractor)
        self.ui.vtkParent.setLayout(layout)


        self.ui.sliceSlider.valueChanged.connect(self.setSliceIdx)
        self.viewer = vtk.vtkImageViewer2()

        self.viewer.SetupInteractor(self.vtkInteractor)
        self.viewer.SetRenderWindow(self.vtkInteractor.GetRenderWindow())

        self.updateSource(source)
    def setPatientDat(self, arr:List[str]):
        self.ui.imageInfo.setText(" ".join(arr))
    
    def renderImage(self):
        if(self.viewer):
            self.viewer.Render()
    def setSliceIdx(self,idx:int):
        if(self.viewer):
            self.viewer.SetSlice(idx)
            self.ui.sliceIdxLabel.setText(f"Slice: {idx+1}/{self.ui.sliceSlider.maximum()+1}")
            self.renderImage()
    def cleanup(self):
        if(self.vtkInteractor):
            self.vtkInteractor.GetRenderWindow().Finalize()

    def updateSource(self, source:Optional[vtk.vtkAlgorithmOutput]):
        self.source = source
        if(source):
            self.viewer.SetInputConnection(source)
            self.ui.sliceSlider.setValue(0)
            self.ui.sliceSlider.setMaximum(self.viewer.GetSliceMax())
            self.ui.sliceIdxLabel.setText(f"Slice: 1/{self.ui.sliceSlider.maximum()+1}")
            self.viewer.GetRenderer().ResetCamera()
            self.viewer.Render()
        else:
            self.viewer.SetInputConnection(None)
        self.renderImage()




    def showErrorMessage(self, title, desc):
        QMessageBox.critical(self, title, desc)




