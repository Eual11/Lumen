from typing import List, Optional,Tuple
from enum import Enum
from PySide6.QtWidgets import QVBoxLayout, QWidget, QMessageBox
from typing import TypedDict
from numpy import spacing
import numpy
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

from core.SegmentOperationCommand import RegionGrowCommand
from utils.utils import numpyArrToVtkImageData

from .ImageViewerUI import Ui_ImageViewerUI
from core.Segment import Segment

class SegmentActorInfo(TypedDict):
    actor: vtk.vtkImageSlice
    mapper: vtk.vtkImageResliceMapper
    lut: vtk.vtkLookupTable

class ViewerMode(Enum):
    NAVIGATION = 1 
    PAINT = 2
    ERASE = 3
    SEED_PLACEMENT = 4

class DicomViewer(QWidget):
    def __init__(self, source: Optional[vtk.vtkAlgorithmOutput] = None, parent=None):
        super().__init__(parent)

        self.ui = Ui_ImageViewerUI()
        self.ui.setupUi(self)

        self.vtkInteractor = QVTKRenderWindowInteractor(self.ui.vtkParent)
        layout = QVBoxLayout()
        layout.addWidget(self.vtkInteractor)
        self.ui.vtkParent.setLayout(layout)

        self.renderer = vtk.vtkRenderer()
        self.render_window = self.vtkInteractor.GetRenderWindow()

        #Testing interactor events
        self.render_window.GetInteractor().AddObserver(vtk.vtkCommand.LeftButtonPressEvent, self.handle_mouse_movement)
        self.render_window.GetInteractor().AddObserver(vtk.vtkCommand.LeftButtonPressEvent, self.handle_left_click)
        self.render_window.GetInteractor().AddObserver(vtk.vtkCommand.LeftButtonReleaseEvent, self.handle_left_release)
        self.render_window.AddRenderer(self.renderer)

        self.mapper = vtk.vtkImageResliceMapper()
        self.mapper.SliceFacesCameraOff()
        self.mapper.SliceAtFocalPointOff()
        self.slice_actor = vtk.vtkImageSlice()
        self.slice_actor.SetMapper(self.mapper)
        self.renderer.AddViewProp(self.slice_actor)

        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.vtkInteractor.SetInteractorStyle(vtk.vtkInteractorStyleImage())

        self.ui.sliceSlider.valueChanged.connect(self.setSliceIdx)

        self.spacing = (1.0, 1.0, 1.0)
        self.extent = (0, 0, 0, 0, 0, 0)
        self.origin = (0.0, 0.0, 0.0)

        self.slice_index = 0


        self.segment_overlay_masks: dict[Segment, SegmentActorInfo] = {}

        self.selected_segment: Optional[Segment] = None
        self.viewer_mode = ViewerMode.NAVIGATION

        self.seed_placement_command: Optional[RegionGrowCommand] = None

        self.is_painting = False

        self.updateSource(source)

    def setPatientDat(self, arr: List[str]):
        self.ui.imageInfo.setText(" ".join(arr))

    def renderImage(self):
        self.render_window.Render()

    def setSliceIdx(self, idx: int):
        if self.mapper:
            z = self.origin[2] + idx * self.spacing[2]
            self.slice_index = z

            plane = vtk.vtkPlane()
            plane.SetOrigin(self.origin[0], self.origin[1], z)
            plane.SetNormal(0, 0, 1)

            self.mapper.SetSlicePlane(plane)
            for value in self.segment_overlay_masks.values():
                mapper = value['mapper']
                mapper.SetSlicePlane(plane)
                mapper.Update()
            self.ui.sliceIdxLabel.setText(f"Slice: {idx + 1}/{self.ui.sliceSlider.maximum() + 1}")
            self.renderImage()

    def cleanup(self):
        self.vtkInteractor.GetRenderWindow().Finalize()

    def updateSource(self, source: Optional[vtk.vtkAlgorithmOutput]):
        self.source = source
        if source:
            self.mapper.SetInputConnection(source)
            source.GetProducer().Update()
            image_data = source.GetProducer().GetOutput()

            self.spacing = image_data.GetSpacing()
            self.origin = image_data.GetOrigin()
            self.extent = image_data.GetExtent()

            zmin, zmax = self.extent[4], self.extent[5]


            self.ui.sliceSlider.setMinimum(zmin)
            self.ui.sliceSlider.setMaximum(zmax)
            self.ui.sliceSlider.setValue(zmin)
            self.setSliceIdx(zmin)

            self.renderer.ResetCamera()
            self.renderImage()
        else:
            self.mapper.SetInputConnection(None)
        self.seed_placement_command = None
        self.clear_renderer()
        self.renderer.Clear()
    def add_segment_overlay(self,segment:Segment):
        mapper = vtk.vtkImageResliceMapper()
        img_data = numpyArrToVtkImageData(segment.mask, self.spacing, vtk.VTK_CHAR)
        mapper.SetInputData(img_data)

        mapper.SliceFacesCameraOff()
        mapper.SliceAtFocalPointOff()

        lut = vtk.vtkLookupTable()
        lut.SetNumberOfTableValues(2)
        lut.SetRange(0,1)
        lut.Build()
        lut.SetTableValue(0,0.0,0.0,0.0,0.0)
        cols =[c/255.0 for c in segment.color] 
        lut.SetTableValue(1,cols[0],cols[1], cols[2],0.5)

        actor = vtk.vtkImageSlice()
        actor.SetMapper(mapper)
        actor.GetProperty().SetLookupTable(lut)
        actor.GetProperty().UseLookupTableScalarRangeOn()

        self.segment_overlay_masks[segment] = {
            "actor": actor,
            "mapper": mapper,
            "lut":lut
        }

        self.renderer.AddViewProp(actor)
        self.render_window.Render()




    def remove_segment_overlay(self,segment:Segment):
        info = self.segment_overlay_masks[segment]
        self.renderer.RemoveActor(info['actor'])
        del self.segment_overlay_masks[segment]
        self.seed_placement_command = None

        self.render_window.Render()
    def set_segment_visibility(self, segment:Segment, value):
        segment_info = self.segment_overlay_masks[segment]
        segment_info['actor'].SetVisibility(value)

        self.render_window.Render()
    def set_segment_color(self, segment:Segment, value:Tuple[int,int,int]):
        segment_info = self.segment_overlay_masks[segment]
        lut = segment_info['lut']
        cols = [c/255.0 for c in value]
        lut.SetTableValue(1, cols[0], cols[1], cols[2],0.5)
        lut.Modified()
        self.render_window.Render()
    def update_segment_mask(self, segment:Segment):
        segment_info = self.segment_overlay_masks.get(segment, None)
        if not segment_info:
            return

        img_data = numpyArrToVtkImageData(segment.mask, self.spacing, vtk.VTK_CHAR)

        mapper = segment_info['actor'].GetMapper()
        mapper.SetInputData(img_data)
        mapper.Update()
    def set_selected_segment(self,segment):
        self.selected_segment = segment


        self.render_window.Render()
    def set_viewer_mode(self,mode:ViewerMode):
        self.viewer_mode = mode



    def showErrorMessage(self, title, desc):
        QMessageBox.critical(self, title, desc)
    def handle_left_click(self,obj, event):
        # perform region growing
        if self.viewer_mode == ViewerMode.SEED_PLACEMENT:
            self.region_grow_segment(obj)
        if self.viewer_mode == ViewerMode.PAINT or self.viewer_mode == ViewerMode.ERASE:
            self.is_painting = True
        


    def handle_left_release(self, obj,event):
        #TODO: issue with release event
        self.is_painting = False

    def paint_at_mouse(self, obj):
        x,y = obj.GetEventPosition()
        picker = vtk.vtkCellPicker()
        picker.SetTolerance(0.0005)
        picker.Pick(x,y,self.slice_index, self.renderer)

        world_pos = picker.GetPickPosition()

        x,y,z = [round((world_pos[i]-self.origin[i])/self.spacing[i]) for i in range(len(world_pos))]


        if x <0 or x >self.extent[1] or y <0 or y>self.extent[3] or z <0 or z > self.extent[5]:
            return

        # TODO: add bruh and eraser radius
        if self.viewer_mode == ViewerMode.PAINT and self.is_painting :
            self.paint_segment(x,y,z,10)
        if self.viewer_mode == ViewerMode.ERASE and self.is_painting :
            self.erase_segment(x,y,z,10)


    def handle_mouse_movement(self,obj,event):
        if self.is_painting:
            self.paint_at_mouse(obj)
        #TODO: depending on the orgin interaction mode we will either, do nothing, paint on the mask or set seed positio
    def paint_segment(self, x0:int,y0:int,z0:int, r:int):

        if not self.selected_segment:
            return
        mask = self.selected_segment.mask
        shape = mask.shape
        z,y,x = numpy.ogrid[:shape[0], :shape[1], :shape[2]]

        dist_sq =((x-x0)**2 + (y-y0)**2 <=r**2) & (z == self.slice_index) 

        mask[dist_sq] = 1

        self.update_segment_mask(self.selected_segment)
    def erase_segment(self, x0:int,y0:int,z0:int, r:int):

        if not self.selected_segment:
            return
        mask = self.selected_segment.mask
        shape = mask.shape
        z,y,x = numpy.ogrid[:shape[0], :shape[1], :shape[2]]

        dist_sq =((x-x0)**2 + (y-y0)**2<=r**2) &(z == self.slice_index) 

        mask[dist_sq] = 0

        self.update_segment_mask(self.selected_segment)
    def region_grow_segment(self,obj):
        x,y = obj.GetEventPosition()
        picker = vtk.vtkCellPicker()
        picker.SetTolerance(0.0005)
        picker.Pick(x,y,self.slice_index, self.renderer)

        world_pos = picker.GetPickPosition()

        x,y,z = [round((world_pos[i]-self.origin[i])/self.spacing[i]) for i in range(len(world_pos))]


        if x <0 or x >self.extent[1] or y <0 or y>self.extent[3] or z <0 or z > self.extent[5]:
            return

        
        if self.seed_placement_command and self.selected_segment:
            self.seed_placement_command.seed_list = [(x,y,z)]
            self.seed_placement_command.execute()
            self.update_segment_mask(self.selected_segment)
    def clear_renderer(self):
        actors = self.renderer.GetActors()
        actors.InitTraversal()

        for _ in range(actors.GetNumberOfItems()):
            actor = actors.GetNextActor()
            self.renderer.RemoveActor(actor)
        actors2d = self.renderer.GetActors2D()

        actors2d.InitTraversal()

        for _ in range(actors2d.GetNumberOfItems()):
            actor = actors2d.GetNextActor2D()
            self.renderer.RemoveActor2D(actor)
    def clear_segment_overlays(self):
        for info in self.segment_overlay_masks.values():
            self.renderer.RemoveActor(info['actor'])
        self.segment_overlay_masks.clear()


        

        


        

