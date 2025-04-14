from PySide6.QtWidgets import QVBoxLayout, QWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

from .ImageViewerUI import Ui_ImageViewerUI


class DicomViewer(QWidget):
    def __init__(self,path,parent=None):
        super().__init__(parent)

        self.ui =Ui_ImageViewerUI()
        self.ui.setupUi(self)

        self.reader = vtk.vtkDICOMImageReader()
        self.reader.SetDirectoryName(path)
        self.reader.Update()
        self.viewer = vtk.vtkImageViewer2()
        self.vtkInteractor = QVTKRenderWindowInteractor(self.ui.vtkParent)

        layout = QVBoxLayout()
        layout.addWidget(self.vtkInteractor)
        self.ui.vtkParent.setLayout(layout)

        self.ui.sliceSlider.valueChanged.connect(self.setSliceIdx)
        self.ui.sliceSlider.setMaximum(self.reader.GetDataExtent()[-1])

        self.viewer = vtk.vtkImageViewer2()

        self.viewer.SetupInteractor(self.vtkInteractor)
        self.viewer.SetRenderWindow(self.vtkInteractor.GetRenderWindow())
        self.viewer.SetInputConnection(self.reader.GetOutputPort())

    def renderImage(self):
        self.viewer.Render()
    def setSliceIdx(self,idx:int):
        self.viewer.SetSlice(idx)
        self.renderImage()



