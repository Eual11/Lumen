from PySide6.QtWidgets import QVBoxLayout, QWidget, QMessageBox
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import os

from .ImageViewerUI import Ui_ImageViewerUI


class DicomViewer(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.ui =Ui_ImageViewerUI()
        self.ui.setupUi(self)

        self.reader = None
        self.viewer = vtk.vtkImageViewer2()
        self.vtkInteractor = QVTKRenderWindowInteractor(self.ui.vtkParent)

        layout = QVBoxLayout()
        layout.addWidget(self.vtkInteractor)
        self.ui.vtkParent.setLayout(layout)


        self.ui.sliceSlider.valueChanged.connect(self.setSliceIdx)
        self.viewer = vtk.vtkImageViewer2()

        self.viewer.SetupInteractor(self.vtkInteractor)
        self.viewer.SetRenderWindow(self.vtkInteractor.GetRenderWindow())
    
        if(self.reader):
            self.viewer.SetInputConnection(self.reader.GetOutputPort())
        else:
            self.viewer.SetInputConnection(None)
        self.renderImage()

    def renderImage(self):
        if(self.viewer):
            self.viewer.Render()
    def setSliceIdx(self,idx:int):
        if(self.viewer):
            self.viewer.SetSlice(idx)
            self.renderImage()
    def cleanup(self):
        if(self.reader):
            self.reader = None
        if(self.vtkInteractor):
            self.vtkInteractor.GetRenderWindow().Finalize()

    def loadImage(self,path):
        self.cleanup()

        self.reader = vtk.vtkDICOMImageReader()

        if(not os.path.exists(path)):
            self.showErrorMessage("Directory doesn't exist", f"The dicom directory {path} doesn't exist")
            return

        if(os.path.isdir(path)):
            self.reader.SetDirectoryName(path)
        else:
            self.showErrorMessage("Invalid Path", f"Path is not a directory")
            return

        try:
            self.reader.Update()
        except:
            print("test")


        if(self.reader.GetNumberOfOutputPorts()==0):
            self.showErrorMessage("Error loading DICOM", f"Failed to load DICOM files from {path}")
            return

        if(self.reader):
            self.ui.sliceSlider.setMaximum(self.reader.GetDataExtent()[-1])

        #TODO: add panning and better controls
        self.viewer.SetupInteractor(self.vtkInteractor)
        self.viewer.SetRenderWindow(self.vtkInteractor.GetRenderWindow())


        if(self.reader):
            self.viewer.SetInputConnection(self.reader.GetOutputPort())
        self.renderImage()
    def showErrorMessage(self, title, desc):
        QMessageBox.critical(self, title, desc)




