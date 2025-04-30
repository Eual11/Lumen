from typing import List
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
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.vtkInteractor.SetInteractorStyle(style)

        layout.addWidget(self.vtkInteractor)

        self.setLayout(layout)



        self.renderer = vtk.vtkRenderer()
        self.renderer.GetActiveCamera().SetPosition(0,0,2)
        self.renderer.SetBackground(0.0,0.0,0.0);
        self.renderer.ResetCamera()

        self.vtkWindow = self.vtkInteractor.GetRenderWindow()
        self.vtkWindow.AddRenderer(self.renderer)

        self.interactor = self.vtkWindow.GetInteractor()

        self.actors: List[vtk.vtkActor] = []

        self.volumes: List[vtk.vtkVolume] = []

        self.interactor.Initialize()
        self.interactor.Start()

    def cleanup(self):
        if(self.vtkWindow):
            self.vtkWindow.Finalize()
    def addActor(self, actor:vtk.vtkActor):
        self.actors.append(actor)
        self.renderer.AddActor(actor)
        self.renderer.ResetCamera()
        self.vtkWindow.Render()
    def addVolume(self, volume: vtk.vtkVolume):
        self.renderer.AddVolume(volume)
        self.volumes.append(volume)
        self.renderer.ResetCamera()
        self.vtkWindow.Render()
    def hasActors(self)->bool:
        return len(self.actors)!=0
    def hasVolume(self)->bool:
        return len(self.actors)!=0

    def writeObj(self, filepath):
        if(self.actors==[]):
            return
        appedMapper = vtk.vtkAppendPolyData()

        for actor in self.actors:

            mapper = actor.GetMapper()
            appedMapper.AddInputData(mapper.GetInput())

        appedMapper.Update()

        writer = vtk.vtkOBJWriter()
        writer.SetFileName(filepath)
        writer.SetInputConnection(appedMapper.GetOutputPort())
        writer.Write()

    def reset(self):
        for actor in self.actors:
            self.renderer.RemoveActor(actor)
        for volume in self.volumes:
            self.renderer.RemoveVolume(volume)
        self.actors.clear()
        self.volumes.clear()
        self.vtkWindow.Render()














