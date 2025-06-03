from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QSpinBox,
    QDialogButtonBox, QGroupBox, QHBoxLayout
)

from app.widgets.DicomViewer import ViewerMode
from core.LumenCore import Lumen
from core.SegmentOperationCommand import FillHolesCommand


class FillHolesDialog(QDialog):
    def __init__(self, lumen_core: Lumen, parent=None):
        super().__init__(parent)
        self.lumen_core = lumen_core
        self.setWindowTitle("Fill Holes in Segmentation")

        # Radius input
        self.radius_input = QSpinBox()
        self.radius_input.setRange(1, 50)
        self.radius_input.setValue(2)

        # Radius layout
        radius_layout = QHBoxLayout()
        radius_layout.addWidget(QLabel("Structuring Element Radius:"))
        radius_layout.addWidget(self.radius_input)

        group_box = QGroupBox("Morphological Operation Settings")
        group_layout = QVBoxLayout()
        group_layout.addLayout(radius_layout)
        group_box.setLayout(group_layout)

        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(group_box)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_radius(self):
        return self.radius_input.value()

    def accept(self):
        radius = self.get_radius()
        segment = self.lumen_core.get_selected_segment()
        if segment:
            cmd = FillHolesCommand(
                image=self.lumen_core.get_pipeline_output_data(),
                segment=segment,
                radius=radius,
                op="add"
            )
            cmd.execute()

        return super().accept()

    def reject(self):
        return super().reject()

def create_fill_holes_dialog(lumen_core:Lumen):
    selected_segment = lumen_core.get_selected_segment()
    if not selected_segment:
        return

    dialog = FillHolesDialog(lumen_core)

    dialog.exec()
