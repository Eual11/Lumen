from vtk import vtkDataArray, vtkImageData, vtkVersion, VTK_INT
from vtkmodules.util import numpy_support
from SimpleITK import Image, GetArrayFromImage, GetImageFromArray

# TODO: support for image type casting
def vtkImageToSITKImage(vtk_img: vtkImageData)->Image:

    """Convert a VTK image to a  SimpleITK image, via VTK numpy_support."""
    vtk_array = vtk_img.GetPointData().GetScalars()


    np_data = numpy_support.vtk_to_numpy(vtk_array)

    # reversed dimentions (x,y,z ) -> (z,y,x)

    dims = vtk_img.GetDimensions()[::-1]

    spacing = vtk_img.GetSpacing()
    direction = vtk_img.GetDirectionMatrix()

    origin = vtk_img.GetOrigin()

    np_data.shape = dims

    sitk_image = GetImageFromArray(np_data)

    sitk_image.SetSpacing(spacing)
    sitk_image.SetOrigin(origin)



    if int(vtkVersion.GetVTKMajorVersion())  >= 9:

        d = []

        for y in range(3):
            for x in range(3):
                d.append(-direction.GetElement(y,x))
        sitk_image.SetDirection(d)


    return sitk_image


def vtkarrayToVtkImageData(vtk_arr:vtkDataArray, shape, spacing, origin=(0,0,0))->vtkImageData:
    """Convert a SimpleITK image to a VTK image, via numpy."""
    img:vtkImageData = vtkImageData()

    img.SetSpacing(spacing)
    img.SetDimensions(shape)
    img.SetOrigin(origin)
    img.GetPointData().SetScalars(vtk_arr)
    img.Modified()

    return img


def SITKImageTOVtkImageData(sitk_img: Image)->vtkImageData:
    numpy_arr = GetArrayFromImage(sitk_img)
    numpy_shape = numpy_arr.shape
    vtk_arr = numpy_support.numpy_to_vtk(numpy_arr.ravel(), deep=False, array_type=VTK_INT)
    return vtkarrayToVtkImageData(vtk_arr, numpy_shape[::-1], sitk_img.GetSpacing())





    


