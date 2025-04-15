from PySide6.QtWidgets import QVBoxLayout, QWidget

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk


class Renderer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frame = QWidget()
        #laout for frame
        layout = QVBoxLayout()

        self.vtkInteractor = QVTKRenderWindowInteractor(self)

        layout.addWidget(self.vtkInteractor)

        self.setLayout(layout)



        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(0.0,0.0,0.0);

        self.vtkWindow = self.vtkInteractor.GetRenderWindow()
        self.vtkWindow.AddRenderer(self.renderer)

        self.interactor = self.vtkWindow.GetInteractor()


        ##TEST:
        cube = vtk.vtkCubeSource()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cube.GetOutputPort())

        actor = vtk.vtkActor()

        actor.SetMapper(mapper)

        self.renderer.AddActor(actor)




        self.interactor.Initialize()
        self.interactor.Start()

    def cleanup(self):
        if(self.vtkWindow):
            self.vtkWindow.Finalize()













