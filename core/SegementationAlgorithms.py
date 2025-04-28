from Segment import Segement
import SimpleITK as sitk

from utils.utils import vtkImageToSITKImage

from vtk import vtkImageData

"""Abstractions for SITK Segementation Algorithms to work on Segements """

class ThresholdFilter:
    lower_threshold:int
    upper_threshold:int
    inside_value:int
    outside_value:int

    _filter: sitk.BinaryThresholdImageFilter

    def __init__(self, lower_threshold:int =0, upper_threshold = 255, inside_value:int=1, outside_value:int =0) -> None:
       self.lower_threshold = lower_threshold
       self.upper_threshold = upper_threshold
       self.inside_value = inside_value 
       self.outside_value = outside_value 
       self._filter = sitk.BinaryThresholdImageFilter()

       
    def Execute(self, image:vtkImageData,segement:Segement, op:str ="add"):

       self._filter.SetLowerThreshold(self.lower_threshold) 
       self._filter.SetUpperThreshold(self.upper_threshold) 
       self._filter.SetInsideValue(self.inside_value) 
       self._filter.SetOutsideValue(self.outside_value)

       sitk_img:sitk.Image   =  vtkImageToSITKImage(image)
       sitk_img = self._filter.Execute(sitk_img) 

       segement.apply_mask_update(sitk.GetArrayViewFromImage(sitk_img), op) 
       

 
