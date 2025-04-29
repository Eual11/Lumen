from SimpleITK import Cast, GetArrayFromImage, MedianImageFilter, RescaleIntensity, WriteImage, sitkUInt16, sitkUInt8

import vtk

from utils.utils import SITKImageTOVtkImageData, vtkImageToSITKImage


import vtkmodules.all as vtk
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase

class MyCustomImageFilter(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(
            self,
            nInputPorts=1,
            inputType='vtkImageData',
            nOutputPorts=1,
            outputType='vtkImageData'
        )

    def RequestData(self, request, inInfo, outInfo):
        # Get input and output
        input_image = vtk.vtkImageData.GetData(inInfo[0])
        output_image = vtk.vtkImageData.GetData(outInfo)

        # Shallow copy input to output as a starting point
        output_image.ShallowCopy(input_image)

        # Now do something custom
        return 1  # success
class MedianFilter(VTKPythonAlgorithmBase):

    def __init__(self):

        self._filter = MedianImageFilter()
        self._filter.SetRadius(1)
        VTKPythonAlgorithmBase.__init__(
            self,
            nInputPorts=1,
            inputType="vtkImageData",
            nOutputPorts=1,
            outputType="vtkImageData"
        )


    def RequestData(self, request, inInfo, outInfo):

        input_data = vtk.vtkImageData.GetData(inInfo[0])
        out_data = vtk.vtkImageData.GetData(outInfo)

        sitk_image = vtkImageToSITKImage(input_data)

        sitk_image = self._filter.Execute(sitk_image)

        vtk_image = SITKImageTOVtkImageData(sitk_image)
        out_data.DeepCopy(vtk_image)


        return 1


