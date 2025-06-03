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

       sitk_arr =  sitk.GetArrayViewFromImage(sitk_img)
       sitk_arr = sitk_arr.reshape(sitk_img.GetSize()[::-1])



       self.segment.apply_mask_update(sitk_arr, self.operation) 
       segment_meta_data = self.segment.meta_data 

       lower = segment_meta_data.get("lower_threshold", float('inf')) 
       upper = segment_meta_data.get("upper_threshold", float('-inf')) 

       segment_meta_data["lower_threshold"] =min(self.lower_threshold, lower) 
       segment_meta_data["upper_threshold"] = max(self.upper_threshold, upper) 

class RegionGrowCommand(SegmentOperationCommand):
    lower_bound:int
    upper_bound:int 
    inside_value:int
    outside_value:int 
    _image:vtkImageData

    operation:str

    def __init__(self, image:vtkImageData, segment:Segment,  lower_bound:int, upper_bound:int, seed_list, op = "add", inside_value:int =1, outside_value:int =0):
        super().__init__(segment)

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self.inside_value = inside_value
        self.outside_value = outside_value

        self.operation = op

        self._filter = sitk.ConnectedThresholdImageFilter()

        self._image = image
        self.seed_list = seed_list

    def execute(self):

        self._filter.SetLower(self.lower_bound)
        self._filter.SetUpper(self.upper_bound)
        self._filter.SetSeedList(self.seed_list)
        self._filter.SetReplaceValue(1)

        sitk_img = vtkImageToSITKImage(self._image)

        sitk_img:sitk.Image = self._filter.Execute(sitk_img)

        sitk_arr = sitk.GetArrayFromImage(sitk_img)

        sitk_arr = sitk_arr.reshape(sitk_img.GetSize()[::-1])

        self.segment.apply_mask_update(sitk_arr, self.operation)
        segment_meta_data = self.segment.meta_data 

        lower = segment_meta_data.get("lower_threshold", float('inf')) 
        upper = segment_meta_data.get("upper_threshold", float('-inf')) 

        segment_meta_data["lower_threshold"] =min(self.lower_bound, lower) 
        segment_meta_data["upper_threshold"] = max(self.upper_bound, upper) 

class ConnectedRegionGrowCommand(SegmentOperationCommand):
    radius:int
    iterations:int
    multiplier:float
    _image:vtkImageData

    operation:str

    def __init__(self, image:vtkImageData, segment:Segment, radius:int ,multiplier:float,iterations:int, seed_list, op = "add"):
        
        super().__init__(segment)

        self.radius = radius 
        self.iterations = iterations
        self.multiplier = multiplier

        self.operation = op

        self._filter = sitk.ConfidenceConnectedImageFilter()

        self._image = image
        self.seed_list = seed_list

    def execute(self):

        self._filter.SetInitialNeighborhoodRadius(self.radius)
        self._filter.SetMultiplier(self.multiplier)
        self._filter.SetNumberOfIterations(self.iterations)

        self._filter.SetSeedList(self.seed_list)
        self._filter.SetReplaceValue(1)

        sitk_img = vtkImageToSITKImage(self._image)

        sitk_img:sitk.Image = self._filter.Execute(sitk_img)

        sitk_arr = sitk.GetArrayFromImage(sitk_img)

        sitk_arr = sitk_arr.reshape(sitk_img.GetSize()[::-1])

        self.segment.apply_mask_update(sitk_arr, self.operation)

class FillHolesCommand(SegmentOperationCommand):
    radius:int

    operation:str

    def __init__(self, image:vtkImageData, segment:Segment, radius:int , op = "add"):
        
        super().__init__(segment)

        self.radius = radius 

        self.operation = op

        self._filter = sitk.BinaryMorphologicalClosingImageFilter()

        self._image = image

    def execute(self):

        sitk_img = vtkImageToSITKImage(self._image)

        vector_radius = (self.radius,self.radius,self.radius)
        self._filter.SetKernelRadius(vector_radius)
        self._filter.SetKernelType(sitk.sitkBall)

        sitk_img:sitk.Image = self._filter.Execute(sitk_img)


        sitk_arr = sitk.GetArrayFromImage(sitk_img)

        sitk_arr = sitk_arr.reshape(sitk_img.GetSize()[::-1])

        self.segment.apply_mask_update(sitk_arr, self.operation)




