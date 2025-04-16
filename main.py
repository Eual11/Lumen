from ntpath import getatime
import sys
import time
from types import DynamicClassAttribute
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtWidgets import QFileDialog
from PySide6 import QtCore
from vtk import vtkActor, vtkColorTransferFunction, vtkCubeSource, vtkFixedPointVolumeRayCastMapper, vtkFlyingEdges3D, vtkGPUVolumeRayCastMapper, vtkImageFlip, vtkImageGaussianSmooth, vtkImageMedian3D, vtkImageSobel3D, vtkImageThreshold, vtkMarchingCubes, vtkOutputWindow, vtkPiecewiseFunction, vtkPolyDataMapper, vtkVolume, vtkVolumeProperty
from app import LumenMainWindow
from app.widgets import Renderer
from app.widgets.DicomViewer import DicomViewer

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from core import DicomLoader, DymanicPipeline
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = LumenMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.loader = DicomLoader.DicomLoader()



        self.view = DicomViewer(self.loader.get_output_port())
        self.renderer = Renderer.Renderer()
        self.filter = None

        self.ui.vtkContainer.addWidget(self.view)
        self.ui.vtkContainer.addWidget(self.renderer)




        self.ui.loadBtn.clicked.connect(lambda: self.load(0))
        self.ui.renderBtn.clicked.connect(lambda: self.renderBtn(self.ui.rendererSelect.currentIndex()))
        self.ui.resetBtn.clicked.connect(self.resetBtn)
        self.ui.saveObjBtn.clicked.connect(self.saveBtn)

    def closeEvent(self, event) -> None:
        self.view.cleanup()
        self.renderer.cleanup()
        return super().closeEvent(event)

    @QtCore.Slot()
    def load(self, n):

        dir = QFileDialog.getExistingDirectory(None, "Load Dicom Imagej")
        if(dir and n==0):
            self.loader.load_imge(dir)
            self.filter = DymanicPipeline.DymanicPipeline(self.loader.get_output_port())

            if(self.ui.enableThr.isChecked()):
                threshold = vtkImageThreshold()
                threshold.ThresholdBetween(self.ui.minThresholdSpinbox.value(), self.ui.maxThresholdSpinbox.value())
                threshold.ReplaceOutOn()
                threshold.SetOutValue(0)
                self.filter.add_filter(threshold)


            self.view.updateSource(self.filter.get_ouput_port())
            self.view.setPatientDat(self.loader.get_medical_property())
    @QtCore.Slot()
    def resetBtn(self):
        self.renderer.reset()
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
            self.renderVolume(n)
    @QtCore.Slot()
    def saveBtn(self):
        path =""
        path = QFileDialog.getExistingDirectory(None,"Save Model")
        if not path:
            return

        modelName = "model"+str(time.time())+".obj"

        filename = QtCore.QDir(path).filePath(modelName)

        self.renderer.writeObj(filename)

        QMessageBox.information(self,"Operation Completed", "Model has been saved!")
    def renderVolume(self, n:int):

        self.ui.saveObjBtn.setDisabled(True)
        
        mapper = vtkFixedPointVolumeRayCastMapper()
        if(n==3):
            mapper = vtkGPUVolumeRayCastMapper()
        if(self.filter):
            mapper.SetInputConnection(self.filter.get_ouput_port())

        color_tf = vtkColorTransferFunction()
        opacity_transfer_function = vtkPiecewiseFunction()


        opacity_transfer_function.AddPoint(-1000, 0.0)  # Air/lung = transparent
        opacity_transfer_function.AddPoint(-300,  0.1)  # Fat = transparent
        opacity_transfer_function.AddPoint(-100,  0.2) # Slight fat/muscle transition
        opacity_transfer_function.AddPoint(0,     0.0)  # Water
        opacity_transfer_function.AddPoint(150,   0.2)  # Start to fade out bone
        opacity_transfer_function.AddPoint(300,   0.3)  # Bone/contrast = hide
        opacity_transfer_function.AddPoint(1000,   1.0)  # Bone/contrast = hide

        color_tf = vtkColorTransferFunction()

        color_tf.AddRGBPoint(-1000, 0.0, 0.0, 0.0)   # Air = black
        color_tf.AddRGBPoint(-100, 0.6, 0.5, 0.4)    # Fat = brownish
        color_tf.AddRGBPoint(0,    0.8, 0.7, 0.6)    # Water = soft tan
        color_tf.AddRGBPoint(50,   0.9, 0.6, 0.5)    # Muscle = pinkish
        color_tf.AddRGBPoint(100,  1.0, 0.8, 0.7)    # Organs
        color_tf.AddRGBPoint(200,  0.6, 0.6, 0.6)    # Bone/contrast = gray (faded)


        volume_property = vtkVolumeProperty()
        volume_property.SetColor(color_tf)
        volume_property.SetScalarOpacity(opacity_transfer_function)
        volume_property.SetInterpolationTypeToLinear()
        volume_property.ShadeOn()


        volume = vtkVolume()
        volume.SetProperty(volume_property)
        volume.SetMapper(mapper)

        self.renderer.addVolume(volume)

    


    def renderSurface(self, n:int):
        mcube = vtkMarchingCubes()
        if(n==1):
            mcube = vtkFlyingEdges3D()
        if(self.filter):
            mcube.SetInputConnection(self.filter.get_ouput_port())
            if(self.ui.enableThr.isChecked()):
                mcube.SetValue(0,(self.ui.minThresholdSpinbox.value()+self.ui.maxThresholdSpinbox.value())//2)
            else:
                mcube.SetValue(0, 128)

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(mcube.GetOutputPort())

        actor= vtkActor()
        actor.SetMapper(mapper)

        self.renderer.addActor(actor)





    

def main():
    app = QApplication(sys.argv)

    vtkOutputWindow.SetGlobalWarningDisplay(0)

    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())



if(__name__ == "__main__"):
    main()

