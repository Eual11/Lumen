
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QSpinBox,
    QDialogButtonBox, QGroupBox, QHBoxLayout
)

from app.widgets.DicomViewer import ViewerMode
from core.LumenCore import Lumen
from core.SegmentOperationCommand import RegionGrowCommand

class RegionGrowingDialog(QDialog):
    def __init__(self, lumen_core:Lumen, parent=None):
        super().__init__(parent)
        self.lumen_core = lumen_core
        self.setWindowTitle("Segment Region Growing")

        # Threshold Inputs
        self.lower_input = QSpinBox()
        self.lower_input.setRange(0, 10000)
        self.lower_input.setValue(100)

        self.upper_input = QSpinBox()
        self.upper_input.setRange(0, 10000)
        self.upper_input.setValue(500)

        # Ensure lower <= upper
        self.lower_input.valueChanged.connect(
            lambda val: self.upper_input.setMinimum(val))
        self.upper_input.valueChanged.connect(
            lambda val: self.lower_input.setMaximum(val))

        # Layout for inputs
        threshold_group = QGroupBox("Threshold Range")
        threshold_layout = QVBoxLayout()

        lower_layout = QHBoxLayout()
        lower_layout.addWidget(QLabel("Lower Threshold:"))
        lower_layout.addWidget(self.lower_input)

        upper_layout = QHBoxLayout()
        upper_layout.addWidget(QLabel("Upper Threshold:"))
        upper_layout.addWidget(self.upper_input)

        threshold_layout.addLayout(lower_layout)
        threshold_layout.addLayout(upper_layout)
        threshold_group.setLayout(threshold_layout)

        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok| QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(threshold_group)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_thresholds(self):
        return self.lower_input.value(), self.upper_input.value()

    def accept(self):
        min_thres, max_thres = self.get_thresholds()
        segment = self.lumen_core.get_selected_segment()
        if segment:
            self.lumen_core.viewer.set_viewer_mode(ViewerMode.SEED_PLACEMENT)
            cmd = RegionGrowCommand(self.lumen_core.get_pipeline_output_data(), segment, 0,10000,[],"add")
            cmd.lower_bound = min_thres
            cmd.upper_bound = max_thres

            # passing 
            self.lumen_core.viewer.seed_placement_command = cmd

        return super().accept()

    def reject(self):
        return super().reject()
def create_region_grow_dialog(lumen_core:Lumen):
    selected_segment = lumen_core.get_selected_segment()

    if not selected_segment:
        return

    dialog = RegionGrowingDialog(lumen_core)

    dialog.show()
