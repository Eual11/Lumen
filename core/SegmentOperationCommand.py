from core.Segment import Segment
import SimpleITK as sitk
from utils.utils import vtkImageToSITKImage
from vtk import vtkImageData
class SegmentOperationCommand:
    def __init__(self, segment:Segment) -> None:
        self.segment = segment

    def execute(self):
        raise NotImplementedError


class ThresholdCommand(SegmentOperationCommand):
    lower_threshold:int
    upper_threshold:int
    inside_value:int
    outside_value:int
    _image:vtkImageData
    operation:str

    _filter: sitk.BinaryThresholdImageFilter

    def __init__(self, image:vtkImageData,segment:Segment, op = "add",lower_threshold:int =0, upper_threshold = 255, inside_value:int=1, outside_value:int =0) -> None:
        super().__init__(segment)

        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        self.inside_value = inside_value 
        self.outside_value = outside_value 

        self.operation = op
        self._filter = sitk.BinaryThresholdImageFilter()
        self._image = image


    def execute(self):

       self._filter.SetLowerThreshold(self.lower_threshold) 
       self._filter.SetUpperThreshold(self.upper_threshold) 
       self._filter.SetInsideValue(self.inside_value) 
       self._filter.SetOutsideValue(self.outside_value)

       sitk_img:sitk.Image   =  vtkImageToSITKImage(self._image)
       sitk_img = self._filter.Execute(sitk_img) 

       self.segment.apply_mask_update(sitk.GetArrayViewFromImage(sitk_img), self.operation) 

