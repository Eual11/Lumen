from vtk import vtkDataArray, vtkImageData, VTK_INT
from vtkmodules.util import numpy_support
from SimpleITK import Image, GetArrayFromImage, GetImageFromArray
from LumenTypes import LumenTypes
from numpy import int32

# TODO: support for image type casting
def vtkImageToSITKImageData(vtk_img: vtkImageData, dtype=LumenTypes.INT32 )->Image:
    vtk_array = vtk_img.GetPointData().GetScalars()
    shape = vtk_img.GetDimensions()[::-1]
    numpy_arr = numpy_support.vtk_to_numpy(vtk_array)
    numpy_arr = numpy_arr.reshape(shape)

    if(dtype == LumenTypes.INT32):
        numpy_arr = numpy_arr.astype(int32)
    img = GetImageFromArray(numpy_arr)
    img.SetOrigin(vtk_img.GetOrigin())
    img.SetSpacing(vtk_img.GetSpacing())

    return img

def vtkarrayToVtkImageData(vtk_arr:vtkDataArray, shape, spacing, origin=(0,0,0))->vtkImageData:
    
    img:vtkImageData = vtkImageData()

    img.SetSpacing(spacing)
    img.SetDimensions(shape)
    img.SetOrigin(origin)
    img.GetPointData().SetScalars(vtk_arr)

    return img


def SITKImageTOVtkImageData(sitk_img: Image)->vtkImageData:
    numpy_arr = GetArrayFromImage(sitk_img)
    numpy_shape = numpy_arr.shape
    vtk_arr = numpy_support.numpy_to_vtk(numpy_arr.ravel(order='F'), deep=True, array_type=VTK_INT)
    return vtkarrayToVtkImageData(vtk_arr, numpy_shape[::-1], sitk_img.GetSpacing())





    


