from PySide6.QtWidgets import (
    QCheckBox, QDialog, QVBoxLayout, QLabel, QSlider,
    QDialogButtonBox
)
from PySide6.QtCore import Qt


class FillHolesActorDialog(QDialog):
    def __init__(self, lumen_core, parent=None):
        super().__init__(parent)
        self.lumen_core = lumen_core
        self.setWindowTitle("Fill Holes in Selected Actor")

        # Slider for Hole Size (0.0 to 1000.0 mm2)
        self.hole_radius_slider = QSlider(Qt.Orientation.Horizontal)
        self.hole_radius_slider.setRange(1, 1000)
        self.hole_radius_slider.setValue(100)
        self.hole_radius_slider.valueChanged.connect(self.update_label)

        self.label = QLabel("Hole Size: 100.0")

        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.hole_radius_slider)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def update_label(self):
        value = self.hole_radius_slider.value()
        self.label.setText(f"Hole Size: {value:.1f}")

    def accept(self):
        hole_radius = float(self.hole_radius_slider.value())
        self.lumen_core.renderer.fill_selected_actor_holes(hole_radius)

        return super().accept()

def create_fill_holes_actor_dialog(lumen_core):
    selected_actor = lumen_core.renderer.selected_actor
    if not selected_actor:
        return

    dialog = FillHolesActorDialog(lumen_core)
    dialog.exec()
