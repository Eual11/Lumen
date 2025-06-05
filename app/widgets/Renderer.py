from typing import List, TypedDict
from PySide6.QtWidgets import QVBoxLayout, QWidget

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

class ActorInfo(TypedDict):
    name:str
    box_widget: vtk.vtkBoxWidget
    visible:bool
    transform_enabled:bool

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

        self.actors: dict[vtk.vtkActor, ActorInfo] = {}
        self.selected_actor = -1


        self.volumes: dict[vtk.vtkVolume, ActorInfo] = {}

        self.interactor.Initialize()
        self.interactor.Start()

    def cleanup(self):
        if(self.vtkWindow):
            self.vtkWindow.Finalize()
    def addActor(self, actor:vtk.vtkActor, box_widget:vtk.vtkBoxWidget):
        info:ActorInfo = {
            'name':'Actor',
            'box_widget': box_widget,
            'visible': True,
            'transform_enabled': False
                          }
        self.actors[actor] = info 
        self.renderer.AddActor(actor)
        self.renderer.ResetCamera()
        self.vtkWindow.Render()
    def addVolume(self, volume: vtk.vtkVolume, box_widget:vtk.vtkBoxWidget):
        info:ActorInfo = {
            'name':'Actor',
            'box_widget': box_widget,
            'visible': True,
            'transform_enabled': False
            }

        self.volumes[volume] = info
        self.renderer.AddVolume(volume)
        self.renderer.ResetCamera()
        self.vtkWindow.Render()
    def hasActors(self)->bool:
        return len(self.actors)!=0
    def hasVolume(self)->bool:
        return len(self.actors)!=0

    def writeObj(self, filepath):
        if(not self.actors):
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
    def set_actor_transform(self, actor:vtk.vtkActor, value:bool):
        info = self.actors[actor]
        info['transform_enabled'] = value
        if value:
            info['box_widget'].On()
        else:
            info['box_widget'].Off()
        
    def set_actor_visibility(self, actor:vtk.vtkActor, value:bool):
        info = self.actors[actor]
        info['visible'] = value
        actor.SetVisibility(value)
        if not value:
            info['box_widget'].Off()
        self.vtkWindow.Render()
        
    

    def set_selected_actor(self, idx:int):
        self.selected_actor = idx

    
    def reset(self):
        # Remove all actors
        for actor in list(self.actors.keys()):
            self.renderer.RemoveActor(actor)

        # Remove all volumes
        for volume in list(self.volumes.keys()):
            self.renderer.RemoveVolume(volume)

        # Disable and clean up all actor widgets
        for actor, info in list(self.actors.items()):
            widget = info.get('box_widget')
            if widget:
                widget.SetEnabled(False)
                if widget.HasObserver(vtk.vtkCommand.InteractionEvent):
                    widget.RemoveAllObservers()
                widget.SetInteractor(None)

        # Disable and clean up all volume widgets
        for volume, info in list(self.volumes.items()):
            widget = info.get('box_widget')
            if widget:
                widget.SetEnabled(False)
                if widget.HasObserver(vtk.vtkCommand.InteractionEvent):
                    widget.RemoveAllObservers()
                widget.SetInteractor(None)

        # Clear both dictionaries
        self.actors.clear()
        self.volumes.clear()

        # Force re-render
        self.vtkWindow.Render()









