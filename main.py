from ntpath import getatime
import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtWidgets import QFileDialog
from PySide6 import QtCore
from vtk import vtkActor, vtkColorTransferFunction, vtkCubeSource, vtkFixedPointVolumeRayCastMapper, vtkFlyingEdges3D, vtkGPUVolumeRayCastMapper, vtkImageFlip, vtkImageGaussianSmooth, vtkImageMedian3D, vtkImageSobel3D, vtkImageThreshold, vtkMarchingCubes, vtkOutputWindow, vtkPiecewiseFunction, vtkPolyDataMapper, vtkVolume, vtkVolumeProperty
from app import LumenMainWindow
from app.widgets import Renderer
from app.widgets.DicomViewer import DicomViewer

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from core import DicomLoader,DymanicPipeline
from core.Filters import  MedianFilter
from core.LumenCore import Lumen, RenderMethods
from core.SegmentOperationCommand import ThresholdCommand
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = LumenMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.lumen_core = Lumen()

        self.view = self.lumen_core.get_viewer()
        self.renderer = self.lumen_core.get_renderer()

        self.ui.vtkContainer.addWidget(self.view)
        self.ui.vtkContainer.addWidget(self.renderer)

        self.ui.loadBtn.clicked.connect(lambda: self.load(0))
        self.ui.renderBtn.clicked.connect(lambda: self.renderBtn(self.ui.rendererSelect.currentIndex()))
        self.ui.resetBtn.clicked.connect(self.resetBtn)
        self.ui.saveObjBtn.clicked.connect(self.saveBtn)

    def closeEvent(self, event) -> None:
        self.lumen_core.cleanup()
        return super().closeEvent(event)

    @QtCore.Slot()
    def load(self, n):

        dir = QFileDialog.getExistingDirectory(None, "Load Dicom Imagej")
        if(dir and n==0):
            self.lumen_core.load_image(dir)

            self.lumen_core.create_segement("test", (255,255,255))

            seg = self.lumen_core.get_segment(0)
            data = self.lumen_core.get_pipeline_output_data()

            cmd = ThresholdCommand(data, seg,op="add")

            cmd.lower_threshold = 400
            cmd.upper_threshold = 3000

            cmd.execute()

            self.lumen_core.render_segment(0, RenderMethods.MARCHING_CUBES)



            
    @QtCore.Slot()
    def resetBtn(self):
        self.lumen_core.reset_renderer()
        self.ui.saveObjBtn.setEnabled(True)
    @QtCore.Slot()
    def renderBtn(self,n:int):
        # 0-> Marching cubes
        # 1 -> flying edges
        # 2 CPU volume ray cast
        #  3 GPU volume raycast
        if(n==0 or n==1):
            self.renderSurface(n)
        elif(n==2 or n==3):
            self.ui.saveObjBtn.setEnabled(False)
            self.renderVolume(n)
    @QtCore.Slot()
    def saveBtn(self):
        path =""
        path = QFileDialog.getExistingDirectory(None,"Save Model")
        if not path:
            return

        modelName = "model"+str(time.time())+".obj"

        filename = QtCore.QDir(path).filePath(modelName)

        self.lumen_core.save_mesh_as(filename)


        QMessageBox.information(self,"Operation Completed", "Model has been saved!")
    def renderVolume(self, n:int):

        
        if(n==2):
            self.lumen_core.renderVolume(RenderMethods.CPU_RAYCASTING)
        else:
            self.lumen_core.renderVolume(RenderMethods.GPU_RAYCASTING)
            


    def renderSurface(self, n:int):

        if(n==0):
            self.lumen_core.renderSurface(RenderMethods.MARCHING_CUBES)
        else:
            self.lumen_core.renderVolume(RenderMethods.FLYING_EDGES)
           

def main():
    app = QApplication(sys.argv)

    # vtkOutputWindow.SetGlobalWarningDisplay(0)

    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())



if(__name__ == "__main__"):
    main()

