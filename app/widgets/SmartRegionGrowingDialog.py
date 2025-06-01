from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QSpinBox, QDoubleSpinBox,
    QDialogButtonBox, QGroupBox, QHBoxLayout
)

from app.widgets.DicomViewer import ViewerMode
from core.LumenCore import Lumen
from core.SegmentOperationCommand import ConnectedRegionGrowCommand


class SmartRegionGrowingDialog(QDialog):
    def __init__(self, lumen_core: Lumen, parent=None):
        super().__init__(parent)
        self.lumen_core = lumen_core
        self.setWindowTitle("Smart Region Growing (Confidence Connected)")

        # Multiplier Input (float)
        self.multiplier_input = QDoubleSpinBox()
        self.multiplier_input.setDecimals(2)
        self.multiplier_input.setRange(0.1, 10.0)
        self.multiplier_input.setSingleStep(0.1)
        self.multiplier_input.setValue(2.5)

        # Iteration Input (int)
        self.iteration_input = QSpinBox()
        self.iteration_input.setRange(1, 50)
        self.iteration_input.setValue(5)

        # Radius Input (int)
        self.radius_input = QSpinBox()
        self.radius_input.setRange(1, 10)
        self.radius_input.setValue(1)

        # Settings Group
        settings_group = QGroupBox("Region Growing Settings")
        settings_layout = QVBoxLayout()

        # Multiplier layout
        mult_layout = QHBoxLayout()
        mult_layout.addWidget(QLabel("Multiplier:"))
        mult_layout.addWidget(self.multiplier_input)

        # Iteration layout
        iter_layout = QHBoxLayout()
        iter_layout.addWidget(QLabel("Iterations:"))
        iter_layout.addWidget(self.iteration_input)

        # Radius layout
        radius_layout = QHBoxLayout()
        radius_layout.addWidget(QLabel("Initial Neighborhood Radius:"))
        radius_layout.addWidget(self.radius_input)

        # Combine layouts
        settings_layout.addLayout(mult_layout)
        settings_layout.addLayout(iter_layout)
        settings_layout.addLayout(radius_layout)
        settings_group.setLayout(settings_layout)

        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(settings_group)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_parameters(self):
        return (
            self.multiplier_input.value(),
            self.iteration_input.value(),
            self.radius_input.value()
        )

    def accept(self):
        multiplier, iterations, radius = self.get_parameters()
        segment = self.lumen_core.get_selected_segment()
        if segment:
            cmd = ConnectedRegionGrowCommand(
                self.lumen_core.get_pipeline_output_data(),
                segment,
                0,0,0,[]
            )

            cmd.multiplier = multiplier
            cmd.iterations = iterations
            cmd.radius = radius

            self.lumen_core.viewer.seed_placement_command = cmd

        return super().accept()

    def reject(self):
        return super().reject()


def create_smart_region_grow_dialog(lumen_core: Lumen):
    selected_segment = lumen_core.get_selected_segment()
    lumen_core.viewer.set_viewer_mode(ViewerMode.SEED_PLACEMENT)

    if not selected_segment:
        return

    dialog = SmartRegionGrowingDialog(lumen_core)
    dialog.exec()
