from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QSpinBox,
    QDialogButtonBox, QGroupBox, QHBoxLayout
)

from app.widgets.DicomViewer import ViewerMode
from core.LumenCore import Lumen

class EraserSettingsDialog(QDialog):
    def __init__(self, lumen_core:Lumen, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eraser Settings")
        self.lumen_core = lumen_core

        # Brush radius input
        self.radius_input = QSpinBox()
        self.radius_input.setRange(1, 100)
        self.radius_input.setValue(5)

        radius_layout = QHBoxLayout()
        radius_layout.addWidget(QLabel("Brush Radius:"))
        radius_layout.addWidget(self.radius_input)

        # Depth input
        self.depth_input = QSpinBox()
        self.depth_input.setRange(1, 1000)
        self.depth_input.setValue(1)

        depth_layout = QHBoxLayout()
        depth_layout.addWidget(QLabel("Brush Depth (Slices):"))
        depth_layout.addWidget(self.depth_input)

        # Group box
        group_box = QGroupBox("Paint Settings")
        group_layout = QVBoxLayout()
        group_layout.addLayout(radius_layout)
        group_layout.addLayout(depth_layout)
        group_box.setLayout(group_layout)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(group_box)
        layout.addWidget(buttons)
        self.setLayout(layout)
    def accept(self, /) -> None:
        vals = self.get_values()
        viewer = self.lumen_core.viewer
        viewer.eraser_radius = vals['radius']
        viewer.eraser_depth = vals['depth']
        viewer.set_viewer_mode(ViewerMode.ERASE)
        return super().accept()

    def get_values(self):
        return {
            "radius": self.radius_input.value(),
            "depth": self.depth_input.value()
        }

def create_erase_settings_dialog(lumen_core: Lumen):
    selected_segment = lumen_core.get_selected_segment()

    if not selected_segment:
        return

    dialog = EraserSettingsDialog(lumen_core)
    dialog.exec()
