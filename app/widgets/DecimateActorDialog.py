from PySide6.QtWidgets import (
    QCheckBox, QDialog, QVBoxLayout, QLabel, QSlider,
    QDialogButtonBox
)
from PySide6.QtCore import Qt

class DecimateActorDialog(QDialog):
    def __init__(self, lumen_core, parent=None):
        super().__init__(parent)
        self.lumen_core = lumen_core
        self.setWindowTitle("Decimate Selected Actor")

        # Slider for Target Reduction (0% to 90%)
        self.reduction_slider = QSlider(Qt.Orientation.Horizontal)
        self.reduction_slider.setRange(0, 90)  # In percent
        self.reduction_slider.setValue(50)     # Default 50%
        self.reduction_slider.valueChanged.connect(self.update_label)

        self.preserve_topology_checkbox = QCheckBox("Preserve Topology")
        self.preserve_topology_checkbox.setChecked(True)

        self.label = QLabel("Target Reduction: 50%")

        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.preserve_topology_checkbox)
        layout.addWidget(self.reduction_slider)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def update_label(self):
        value = self.reduction_slider.value()
        self.label.setText(f"Target Reduction: {value}%")

    def accept(self):
        reduction_percent = self.reduction_slider.value()
        preserve_topology = self.preserve_topology_checkbox.isChecked()
        reduction_value = reduction_percent / 100.0

        self.lumen_core.renderer.decimate_selected_actor(reduction_value, preserve_topology)

        return super().accept()

def create_decimate_actor_dialog(lumen_core):
    selected_actor = lumen_core.renderer.selected_actor
    if not selected_actor:
        return

    dialog = DecimateActorDialog(lumen_core)
    dialog.exec()
