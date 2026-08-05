from typing import List, Optional, TypedDict
from PySide6.QtWidgets import QVBoxLayout, QWidget

import utils.vtk_init  # noqa: F401  registers VTK's OpenGL object factories
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkCommonCore import VTK_DOUBLE_MAX, vtkCommand, vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkPlanes
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkClipPolyData, vtkDecimatePro, vtkSmoothPolyDataFilter
from vtkmodules.vtkFiltersModeling import vtkButterflySubdivisionFilter, vtkFillHolesFilter, vtkLinearSubdivisionFilter
from vtkmodules.vtkIOGeometry import vtkOBJWriter, vtkSTLWriter
from vtkmodules.vtkIOImage import vtkJPEGWriter, vtkPNGWriter
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import vtkBoxWidget
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkRenderer, vtkVolume, vtkWindowToImageFilter

class ActorInfo(TypedDict):
    name:str
    box_widget: vtkBoxWidget
    visible:bool
    transform_enabled:bool

class Renderer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frame = QWidget()
        #laout for frame
        layout = QVBoxLayout()

        self.vtkInteractor = QVTKRenderWindowInteractor(self)
        style = vtkInteractorStyleTrackballCamera()
        self.vtkInteractor.SetInteractorStyle(style)

        layout.addWidget(self.vtkInteractor)

        self.setLayout(layout)



        self.renderer = vtkRenderer()
        self.renderer.GetActiveCamera().SetPosition(0,0,2)
        self.renderer.SetBackground(0.0,0.0,0.0);
        self.renderer.ResetCamera()

        self.vtkWindow = self.vtkInteractor.GetRenderWindow()
        self.vtkWindow.AddRenderer(self.renderer)

        self.interactor = self.vtkWindow.GetInteractor()

        self.actors: dict[vtkActor, ActorInfo] = {}
        self.selected_actor: Optional[vtkActor] = None
        self.selected_volume: Optional[vtkVolume] = None


        self.volumes: dict[vtkVolume, ActorInfo] = {}

        self.interactor.Initialize()
        self.interactor.Start()

    def cleanup(self):
        if(self.vtkWindow):
            self.vtkWindow.Finalize()
    def addActor(self, actor:vtkActor, box_widget:vtkBoxWidget):
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
    def addVolume(self, volume: vtkVolume, box_widget:vtkBoxWidget):
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

    def write_selected_actor_obj(self, filepath):
        if self.selected_actor:
            actor = self.selected_actor
            mapper = actor.GetMapper()
            writer = vtkOBJWriter()
            source_filter = mapper.GetInputConnection(0,0).GetProducer()
            writer.SetFileName(filepath)
            writer.SetInputConnection(source_filter.GetOutputPort())
            writer.Write()
    def write_selected_actor_stl(self, filepath):
        if self.selected_actor:
            actor = self.selected_actor
            mapper = actor.GetMapper()
            writer = vtkSTLWriter()
            source_filter = mapper.GetInputConnection(0,0).GetProducer()
            writer.SetFileName(filepath)
            writer.SetInputConnection(source_filter.GetOutputPort())
            writer.Write()


    def writeObj(self, filepath):
        if(not self.actors):
            return
        appedMapper = vtkAppendPolyData()

        for actor in self.actors:

            mapper = actor.GetMapper()
            appedMapper.AddInputData(mapper.GetInput())

        appedMapper.Update()

        writer = vtkOBJWriter()
        writer.SetFileName(filepath)
        writer.SetInputConnection(appedMapper.GetOutputPort())
        writer.Write()

    def writePNG(self, filepath="screenshot.png"):
        png_filter = vtkWindowToImageFilter()
        png_filter.SetInput(self.vtkWindow)
        png_filter.Update()
        writer =  vtkPNGWriter()
        writer.SetFileName(filepath)
        writer.SetInputConnection(png_filter.GetOutputPort())

        writer.Write()

    def writeJPG(self, filepath="screenshot.jpg"):
        png_filter = vtkWindowToImageFilter()
        png_filter.SetInput(self.vtkWindow)
        png_filter.Update()
        writer =  vtkJPEGWriter()
        writer.SetFileName(filepath)
        writer.SetInputConnection(png_filter.GetOutputPort())

        writer.Write()



    def set_actor_transform(self, actor:vtkActor, value:bool):
        info = self.actors[actor]
        info['transform_enabled'] = value
        if value:
            info['box_widget'].On()
        else:
            info['box_widget'].Off()
        
    def set_actor_visibility(self, actor:vtkActor, value:bool):
        info = self.actors[actor]
        info['visible'] = value
        actor.SetVisibility(value)
        if not value:
            info['box_widget'].Off()
        self.vtkWindow.Render()

    def set_volume_transform(self, volume:vtkVolume, value:bool):
        info = self.volumes[volume]
        info['transform_enabled'] = value
        if value:
            info['box_widget'].On()
        else:
            info['box_widget'].Off()
        self.vtkWindow.Render()

    def set_volume_visibility(self, volume:vtkVolume, value:bool):
        info = self.volumes[volume]
        info['visible'] = value
        volume.SetVisibility(value)
        if not value:
            info['box_widget'].Off()
        self.vtkWindow.Render()
        
    

    def set_selected_actor(self,actor:vtkActor):
        if actor and actor in self.actors:
            self.selected_actor = actor
        else:
            self.selected_actor = None

    def set_selected_volume(self,volume:vtkVolume):
        if volume and volume in self.volumes:
            self.selected_volume = volume
        else:
            self.selected_volume = None

    def remove_selected_actor(self):
        self.remove_actor(self.selected_actor)
        self.selected_actor = None
    def remove_selected_volume(self):
        self.remove_volume(self.selected_volume)
        self.selected_volume = None
    def remove_actor(self, actor):
        if actor and actor in self.actors:
            self.renderer.RemoveActor(actor)
            info = self.actors[actor]
            widget = info.get('box_widget')
            if widget:
                widget.SetEnabled(False)
                if widget.HasObserver(vtkCommand.InteractionEvent):
                    widget.RemoveAllObservers()
                widget.SetInteractor(None)
            self.actors.pop(actor)
    def remove_volume(self, volume):
        if volume and volume in self.volumes:
            self.renderer.RemoveVolume(volume)
            info = self.volumes[volume]
            widget = info.get('box_widget')
            if widget:
                widget.SetEnabled(False)
                if widget.HasObserver(vtkCommand.InteractionEvent):
                    widget.RemoveAllObservers()
                widget.SetInteractor(None)
            self.volumes.pop(volume)
    def set_selected_actor_shading(self,idx):
        if self.selected_actor:
            prop = self.selected_actor.GetProperty()
            if idx == 0:
                prop.SetInterpolationToPhong()
            elif idx == 1:
                prop.SetInterpolationToPhong()
            elif idx == 2:
                prop.SetInterpolationToFlat()
            elif idx == 3:
                prop.SetInterpolationToGouraud()
            elif idx == 4 and hasattr(prop, 'SetInterpolationToPBR'):
                prop.SetInterpolationToPBR()
            self.vtkWindow.Render()

    def set_selected_actor_display(self, idx):
        if self.selected_actor:
            prop = self.selected_actor.GetProperty()
            if idx == 0:
                prop.SetRepresentationToSurface()
            elif idx == 1:
                prop.SetRepresentationToPoints()
            elif idx == 2:
                prop.SetRepresentationToWireframe()
            self.vtkWindow.Render()
    def decimate_selected_actor(self,value, preserve_toplogy=True):
        if self.selected_actor:
            actor = self.selected_actor
            color = actor.GetProperty().GetColor()
            mapper = actor.GetMapper()
            source_filter = mapper.GetInputConnection(0,0).GetProducer()
            polydata = source_filter.GetOutputPort()

            decimate = vtkDecimatePro()

            decimate.SetInputConnection(polydata)
            decimate.SetTargetReduction(value)
            if preserve_toplogy:
                decimate.PreserveTopologyOn()
            else:
                decimate.PreserveTopologyOff()
                decimate.SplittingOn()
                decimate.BoundaryVertexDeletionOn()
                decimate.SetMaximumError(VTK_DOUBLE_MAX)

            decimate.Update()

            new_mapper = vtkPolyDataMapper()
            new_mapper.SetInputConnection(decimate.GetOutputPort())

            new_mapper.SetScalarVisibility(0)
            actor.SetMapper(new_mapper)
            actor.GetProperty().SetColor(*color)
            self.vtkWindow.Render()

    def fill_selected_actor_holes(self, hole_radius:float):
        if self.selected_actor:
            actor = self.selected_actor
            color = actor.GetProperty().GetColor()
            mapper = actor.GetMapper()
            source_filter = mapper.GetInputConnection(0,0).GetProducer()
            polydata = source_filter.GetOutputPort()

            filler = vtkFillHolesFilter()

            filler.SetHoleSize(hole_radius)
            filler.SetInputConnection(polydata)
            filler.Update()
            new_mapper = vtkPolyDataMapper()
            new_mapper.SetInputConnection(filler.GetOutputPort())

            new_mapper.SetScalarVisibility(0)
            actor.SetMapper(new_mapper)
            actor.GetProperty().SetColor(*color)
            self.vtkWindow.Render()





    def smooth_selected_actor(self):
        if self.selected_actor:
            actor = self.selected_actor
            color = actor.GetProperty().GetColor()
            mapper = actor.GetMapper()
            source_filter = mapper.GetInputConnection(0,0).GetProducer()
            polydata = source_filter.GetOutputPort()

            smoother = vtkSmoothPolyDataFilter()
            smoother.SetInputConnection(polydata)
            smoother.SetNumberOfIterations(20)
            smoother.Update()

            new_mapper = vtkPolyDataMapper()
            new_mapper.SetInputConnection(smoother.GetOutputPort())

            actor.SetMapper(new_mapper)
            new_mapper.SetScalarVisibility(0)
            actor.GetProperty().SetColor(*color)
    def linear_subdivide_selected_actor(self):
        if self.selected_actor:
            actor = self.selected_actor
            try:
                # Not Implemented
                return
                mapper = actor.GetMapper()
                source_filter = mapper.GetInputConnection(0,0).GetProducer()
                polydata = source_filter.GetOutputPort()

                divider = vtkLinearSubdivisionFilter()
                divider.SetInputConnection(polydata)
                divider.SetNumberOfSubdivisions(2)
                divider.Update()

                new_mapper = vtkPolyDataMapper()
                new_mapper.SetInputConnection(divider.GetOutputPort())

                actor.SetMapper(new_mapper)
            except Exception as e:
                print(f"Subdivision Error {e}")
    def butterfly_subdivide_selected_actor(self):
        if self.selected_actor:
            actor = self.selected_actor
            try:
                # Not Implemented
                return
                mapper = actor.GetMapper()
                source_filter = mapper.GetInputConnection(0,0).GetProducer()
                polydata = source_filter.GetOutputPort()


                butterfly_subdiv = vtkButterflySubdivisionFilter()

                butterfly_subdiv.SetInputData(polydata)
                butterfly_subdiv.SetNumberOfSubdivisions(2)
                butterfly_subdiv.Update()

                new_mapper = vtkPolyDataMapper()
                new_mapper.SetInputConnection(butterfly_subdiv.GetOutputPort())

                actor.SetMapper(new_mapper)
            except Exception as e:
                print(f"Subdivision Error {e}")

    def flip_clipping_planes(self,planes: vtkPlanes) -> vtkPlanes:
        flipped_planes = vtkPlanes()
        flipped_normals = vtkDoubleArray()
        flipped_normals.SetNumberOfComponents(3)
        flipped_normals.SetNumberOfTuples(planes.GetNormals().GetNumberOfTuples())

        for i in range(planes.GetNormals().GetNumberOfTuples()):
            n = planes.GetNormals().GetTuple3(i)
            flipped_normals.SetTuple3(i, -n[0], -n[1], -n[2])

        flipped_planes.SetNormals(flipped_normals)
        flipped_planes.SetPoints(planes.GetPoints())  # origin stays the same
        return flipped_planes

    def clip_selected_actor(self):
        if self.selected_actor:

            actor = self.selected_actor
            color = actor.GetProperty().GetColor()
            # getting incapsulating box widget
            box_widget = self.actors[actor]['box_widget']
            mapper = actor.GetMapper()
            source_filter = mapper.GetInputConnection(0,0).GetProducer()
            polydata = source_filter.GetOutputPort()

            clipper = vtkClipPolyData()
            clipper.SetInputConnection(polydata)

            planes = vtkPlanes()
            
            box_widget.GetPlanes(planes)

            clipper.SetClipFunction(planes)
            clipper.InsideOutOn()
            clipper.Update()
            

            new_mapper = vtkPolyDataMapper()
            new_mapper.SetInputConnection(clipper.GetOutputPort())

            new_mapper.SetScalarVisibility(0)
            actor.SetMapper(new_mapper)
            actor.GetProperty().SetColor(*color)
            box_widget.SetProp3D(actor)
            box_widget.PlaceWidget()

            self.vtkWindow.Render()


    def set_selected_actor_metallic(self, value):
        actor = self.selected_actor
        if actor:
            actor.GetProperty().SetMetallic(value / 100.0)
            self.vtkWindow.Render()

    def set_selected_actor_roughness(self, value):
        actor = self.selected_actor
        if actor:
            actor.GetProperty().SetRoughness(value / 100.0)
            self.vtkWindow.Render()

    def set_selected_actor_specular(self, value):
        actor = self.selected_actor
        if actor:
            actor.GetProperty().SetSpecular(value / 100.0)
            self.vtkWindow.Render()


    def set_selected_actor_base_color(self, r, g, b):
        actor = self.selected_actor
        if actor:
            actor.GetProperty().SetColor(r, g, b)
            self.vtkWindow.Render()

    def set_selected_actor_specular_power(self, value):
        actor = self.selected_actor
        if actor:
            actor.GetProperty().SetSpecularPower(value) 
            self.vtkWindow.Render()




    
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
                if widget.HasObserver(vtkCommand.InteractionEvent):
                    widget.RemoveAllObservers()
                widget.SetInteractor(None)

        # Disable and clean up all volume widgets
        for volume, info in list(self.volumes.items()):
            widget = info.get('box_widget')
            if widget:
                widget.SetEnabled(False)
                if widget.HasObserver(vtkCommand.InteractionEvent):
                    widget.RemoveAllObservers()
                widget.SetInteractor(None)

        # Clear both dictionaries
        self.actors.clear()
        self.volumes.clear()

        self.selected_actor = None

        # Force re-render
        self.vtkWindow.Render()









