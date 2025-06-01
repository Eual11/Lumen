from enum import Enum
from random import randrange
from typing import List, Optional, Tuple
import time
from SimpleITK import GetImageFromArray
from SimpleITK.SimpleITK import Exp
import numpy
from vtkmodules.util import numpy_support
from app.widgets.DicomViewer import DicomViewer
from app.widgets.Renderer import Renderer
from core import DicomLoader, DymanicPipeline

from core.SegmentOperationCommand import ThresholdCommand
from vtk import vtkActor, vtkAlgorithm, vtkColorTransferFunction, vtkCubeSource, vtkFixedPointVolumeRayCastMapper, vtkFlyingEdges3D, vtkGPUVolumeRayCastMapper, vtkImageData, vtkImageFlip, vtkImageGaussianSmooth, vtkImageMedian3D, vtkImageSobel3D, vtkImageThreshold, vtkMarchingCubes, vtkOutputWindow, vtkPiecewiseFunction, vtkPolyDataMapper, vtkVolume, vtkVolumeProperty,VTK_INT

from core.Segment import Segment
from utils.utils import save_numpy_arr_as_png, save_sitk_image, vtkImageToNumpyArr, vtkarrayToVtkImageData


class RenderMethods(Enum):
    MARCHING_CUBES = 'mcubes',
    FLYING_EDGES = 'flying_edges'
    CPU_RAYCASTING = 'cpu_raycasting'
    GPU_RAYCASTING = 'gpu_raycasting'
class ExportFormat(Enum):
    OBJ = 'obj',
    STL = 'stl'


class Lumen:
    def __init__(self) -> None:
        # handles image loading
        self.loader = DicomLoader.DicomLoader()
        
        # Dicom viewer and 3D rendering widgets
        self.viewer = DicomViewer(self.loader.get_output_port())
        self.renderer = Renderer()

        self.image_pipeline = None

        self.segments: List[Segment] = []

        self.selected_segment =-1
        self.segment_name_idx =1
        #Used for rendering
        self.surface_iso_value = 100

    def get_renderer(self):
        return self.renderer
    def get_viewer(self):
        return self.viewer

    def reset_renderer(self):
        self.renderer.reset()
    def set_segment_visibility(self,idx,value):
        if idx <0 or idx >= len(self.segments):
            return
        segment = self.segments[idx]

        segment.visibility = value

        self.viewer.set_segment_visibility(segment, value)
    def set_segment_color(self,idx,color:Tuple[int,int,int]):
        if idx <0 or idx >= len(self.segments):
            return
        segment = self.segments[idx]

        segment.color = color

        self.viewer.set_segment_color(segment, color)
    def get_selected_segment(self):
        if self.selected_segment <0 or self.selected_segment >= len(self.segments):
            return None


        return self.segments[self.selected_segment]
    def set_selected_segment(self, idx:int):
        if idx <0 or idx >= len(self.segments):
            self.selected_segment = -1
            self.viewer.set_selected_segment(None)
        else:
            self.selected_segment = idx
            self.viewer.set_selected_segment(self.segments[self.selected_segment])

 
    def delete_selected_segment(self):
        if self.selected_segment <0 or self.selected_segment >= len(self.segments):
            return
        segment = self.segments[self.selected_segment]
        self.viewer.remove_segment_overlay(segment)
        self.segments.pop(self.selected_segment)
        self.set_selected_segment(-1)
    def render_selected_segment(self, method:RenderMethods):
        if self.selected_segment <0 or self.selected_segment >= len(self.segments):
            return
        self.render_segment(self.selected_segment, method)

    def cleanup(self):
        self.viewer.cleanup()
        self.renderer.cleanup()

    def get_image_size(self):
        extent = self.loader.get_image_dimensions()
        size = (extent[1]-extent[0]+1, extent[3]-extent[2]+1, extent[5]-extent[4]+1)
        return size

    def create_segement(self, name:str="Segment", color:Tuple[int,int,int]=(0,0,0), debug=False):

        # Segements have the same size as the image currently loaded by the image loader
        extent = self.loader.get_image_dimensions()
        if( not (extent[1] or extent[3] or extent[5])):
            return
        #Reversed because Numpy image shape is (depth, height, width)
        size = (extent[1]-extent[0]+1, extent[3]-extent[2]+1, extent[5]-extent[4]+1)[::-1]
        if(not (size[0] or size[1] or size[2])):
            return
        name_exists = name in [s.name for s in self.segments]
        if(name_exists):
            name+=f"{self.segment_name_idx}"
            self.segment_name_idx+=1
        new_segement = Segment(name, size, color)
       
        if(debug):
            print(new_segement)

        self.segments.append(new_segement)
        self.viewer.add_segment_overlay(new_segement)
       
    def get_segment(self,idx:int) -> Segment:
        if 0<=idx<len(self.segments):
            return self.segments[idx]
        else:
            raise IndexError("Segment Index out of bounds")
    def update_selected_segment_overlay_mask(self):
        selected_segment = self.get_selected_segment()
        if not selected_segment:
            return
        self.viewer.update_segment_mask(selected_segment)
    def render_segment(self,idx:int, method:RenderMethods):
        if 0 <= idx < len(self.segments):
            segment = self.segments[idx]
            mask = segment.mask
            img:vtkImageData = self.get_pipeline_output_data()
            shape = img.GetDimensions()
            img_arr = numpy_support.vtk_to_numpy(img.GetPointData().GetScalars())
            dims = img.GetDimensions()
            img_arr = img_arr.reshape(dims[2], dims[1], dims[1])
            final_img = mask*img_arr
            final_img_vtk_array =  numpy_support.numpy_to_vtk(final_img.ravel(), deep=False, array_type=VTK_INT)
            final_vtk_img = vtkarrayToVtkImageData(final_img_vtk_array, shape,img.GetSpacing())
            if method == RenderMethods.MARCHING_CUBES or method == RenderMethods.FLYING_EDGES:
                iso_value = self.surface_iso_value
                if "lower_threshold" in segment.meta_data:
                    iso_value = segment.meta_data['lower_threshold']
                self.renderSurface(method, final_vtk_img,int(iso_value), segment.color)
            else:
                self.renderVolume(final_vtk_img, method)


        else:
            raise IndexError

    def load_image(self, path):

        self.loader.load_imge(path)

        # create image processing pipeline
        self.image_pipeline = DymanicPipeline.DynamicPipeline(self.loader.get_output_port())

        #clearing pre-existing segments
        
        self.viewer.updateSource(self.image_pipeline.get_ouput_port())
        self.viewer.clear_segment_overlays()
        self.segments.clear()
    def get_pipeline_output_port(self):
        if(self.image_pipeline):
            return self.image_pipeline.get_ouput_port()
        else:
            raise ValueError("No Image pipeline setup")
    def get_pipeline_output_data(self):
        if(self.image_pipeline):
            return self.image_pipeline.get_output_data()
        else:
            raise ValueError("No Image pipeline setup")
    def set_isovalue(self,value:int):
        self.surface_iso_value = value

        self.viewer.setPatientDat(self.loader.get_medical_property())
    def renderSurface(self, method:RenderMethods,imgData:Optional[vtkImageData]=None, isoValue = 128, color = (0,255,0)):
        mcube = vtkMarchingCubes()
        if(method == RenderMethods.FLYING_EDGES):
            mcube = vtkFlyingEdges3D()
        if(self.image_pipeline):
            if(imgData):
                mcube.SetInputData(imgData)
            else:
                mcube.SetInputConnection(self.image_pipeline.get_ouput_port())
            mcube.SetValue(0, isoValue)
            mcube.Update()

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(mcube.GetOutputPort())

        # disable scalar visibility to apply actor color
        mapper.SetScalarVisibility(0)

        actor= vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(*[c/255.0 for c in color[0:3]])

        self.renderer.addActor(actor)
    def add_filter(self, filter:vtkAlgorithm, index = None):
        if self.image_pipeline:
            self.image_pipeline.add_filter(filter, index)
    def renderVolume(self,imgData:Optional[vtkImageData], method:RenderMethods):

        
        mapper = vtkFixedPointVolumeRayCastMapper()
        if(method==RenderMethods.GPU_RAYCASTING):
            mapper = vtkGPUVolumeRayCastMapper()
        if imgData :
            mapper.SetInputData(imgData)
        elif(self.image_pipeline):
            mapper.SetInputConnection(self.image_pipeline.get_ouput_port())

        # TODO: customizable opacity transfer and color tranfer point selection

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
    def save_mesh_as(self, filename:str, format:ExportFormat = ExportFormat.OBJ):
        if(format == ExportFormat.OBJ):
            self.renderer.writeObj(filename)
        else:
            # TODO: Save as STL
            pass
    def get_image_range(self):
        if self.image_pipeline:
           img= self.image_pipeline.get_output_data()
           arr = vtkImageToNumpyArr(img) 
           return arr.min(), arr.max() 
        return 0,0
    def get_image_histogram(self,num_bins:int, n_samples:int):
        if not self.image_pipeline:
            return []
        img_min, img_max = self.get_image_range()
        bin_width = (img_max-img_min+1) //num_bins
        x,y,z = self.get_image_size()

        img_arr = vtkImageToNumpyArr(self.image_pipeline.get_output_data())

        histogram_arr = [0]*(num_bins+1)
        for _ in range(n_samples):
            val = img_arr[randrange(z),randrange(y),randrange(x)]
            idx =(val-img_min) // bin_width
            if idx < len(histogram_arr):
                histogram_arr[idx]+=1


        return histogram_arr




