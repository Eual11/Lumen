from vtk import vtkDataArray, vtkImageData, vtkVersion, VTK_INT
from numpy import ndarray
from vtkmodules.util import numpy_support
from SimpleITK import Image, GetArrayFromImage, GetImageFromArray,RescaleIntensity,Cast,sitkUInt16, WriteImage, sitkUInt8

# TODO: support for image type casting
def vtkImageToSITKImage(vtk_img: vtkImageData,)->Image:

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


# save a sitk_img to png, this only support 2D images and 3D image with only a depth of 1


def save_sitk_image(sitk_img:Image, filename):


# Rescale intensities to [0, 255]

    sitk_img = RescaleIntensity(sitk_img)
# Cast to unsigned 8-bit
    rescaled_uint8 = Cast(sitk_img, sitkUInt8)

# Save as PNG
    WriteImage(rescaled_uint8, filename)

    print("saved")

# debug function to save a 2D or 3D with depth of 1 image as a png

def save_numpy_arr_as_png(arr:ndarray, filename="output_image.png"):
    img = GetImageFromArray(arr.reshape(arr.shape[::-1]))

    save_sitk_image(img,filename)


        


