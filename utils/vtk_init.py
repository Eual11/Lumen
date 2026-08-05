"""VTK object-factory registration.
"""

# Render windows, renderers, polydata/image mappers, text rendering.
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# vtkGPUVolumeRayCastMapper / vtkFixedPointVolumeRayCastMapper overrides.
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401
# vtkTextActor glyph rendering.
import vtkmodules.vtkRenderingFreeType  # noqa: F401
# vtkInteractorStyleImage / vtkInteractorStyleTrackballCamera.
import vtkmodules.vtkInteractionStyle  # noqa: F401
