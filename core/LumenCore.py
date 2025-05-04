from enum import Enum
from typing import List, Optional, Tuple
import time
from SimpleITK import GetImageFromArray
from SimpleITK.SimpleITK import Exp
import numpy
from vtkmodules.util import numpy_support
from app.widgets.DicomViewer import DicomViewer
from app.widgets.Renderer import Renderer
from core import DicomLoader, DymanicPipeline

from vtk import vtkActor, vtkAlgorithm, vtkColorTransferFunction, vtkCubeSource, vtkFixedPointVolumeRayCastMapper, vtkFlyingEdges3D, vtkGPUVolumeRayCastMapper, vtkImageData, vtkImageFlip, vtkImageGaussianSmooth, vtkImageMedian3D, vtkImageSobel3D, vtkImageThreshold, vtkMarchingCubes, vtkOutputWindow, vtkPiecewiseFunction, vtkPolyDataMapper, vtkVolume, vtkVolumeProperty,VTK_INT

from core.Segment import Segment
from utils.utils import save_numpy_arr_as_png, save_sitk_image, vtkarrayToVtkImageData


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

    def get_renderer(self):
        return self.renderer
    def get_viewer(self):
        return self.viewer

    def reset_renderer(self):
        self.renderer.reset()

    def cleanup(self):
        self.viewer.cleanup()
        self.renderer.cleanup()
    def create_segement(self, name:str, color:Tuple[int,int,int], debug=False):

        # Segements have the same size as the image currently loaded by the image loader
        extent = self.loader.get_image_dimensions()
        size = (extent[1]-extent[0]+1, extent[3]-extent[2]+1, extent[5]-extent[4]+1)
        new_segement = Segment(name, size, color)

        if(debug):
            print(new_segement)


        self.segments.append(new_segement)
    def get_segment(self,idx:int) -> Segment:
        if 0<=idx<len(self.segments):
            return self.segments[idx]
        else:
            raise IndexError("Segment Index out of bounds")
    def render_segment(self,idx:int, method:RenderMethods):
        if 0 <= idx < len(self.segments):
            segment = self.segments[idx]
            mask = segment.mask
            img:vtkImageData = self.get_pipeline_output_data()
            shape = img.GetDimensions()
            img_arr = numpy_support.vtk_to_numpy(img.GetPointData().GetScalars())
            dims = img.GetDimensions()
            img_arr = img_arr.reshape(dims[0], dims[1], dims[2])
            final_img = mask*img_arr
            final_img_vtk_array =  numpy_support.numpy_to_vtk(final_img.ravel(), deep=False, array_type=VTK_INT)
            if method == RenderMethods.MARCHING_CUBES or method == RenderMethods.FLYING_EDGES:
                final_vtk_img = vtkarrayToVtkImageData(final_img_vtk_array, shape,img.GetSpacing())
                self.renderSurface(method, final_vtk_img)
            else:
                raise NotImplemented


        else:
            raise IndexError

    def load_image(self, path):

        self.loader.load_imge(path)

        # create image processing pipeline
        self.image_pipeline = DymanicPipeline.DynamicPipeline(self.loader.get_output_port())


        self.viewer.updateSource(self.image_pipeline.get_ouput_port())
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

        self.viewer.setPatientDat(self.loader.get_medical_property())
    def renderSurface(self, method:RenderMethods,imgData:Optional[vtkImageData]=None):
        mcube = vtkMarchingCubes()
        if(method == RenderMethods.FLYING_EDGES):
            mcube = vtkFlyingEdges3D()
        if(self.image_pipeline):
            if(imgData):
                mcube.SetInputData(imgData)
            else:
                mcube.SetInputConnection(self.image_pipeline.get_ouput_port())
            mcube.SetValue(0, 128)

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(mcube.GetOutputPort())

        actor= vtkActor()
        actor.SetMapper(mapper)

        self.renderer.addActor(actor)
    def add_filter(self, filter:vtkAlgorithm, index = None):
        if self.image_pipeline:
            self.image_pipeline.add_filter(filter, index)
    def renderVolume(self, method:RenderMethods):

        
        mapper = vtkFixedPointVolumeRayCastMapper()
        if(method==RenderMethods.GPU_RAYCASTING):
            mapper = vtkGPUVolumeRayCastMapper()
        if(self.image_pipeline):
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




