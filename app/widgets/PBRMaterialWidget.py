
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel, QColorDialog, QPushButton
from PySide6.QtCore import Qt

class PBRMaterialWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Metallic
        self.metallicSlider = QSlider(Qt.Horizontal)
        self.metallicSlider.setRange(0, 100)
        self.metallicSlider.setValue(0)
        layout.addWidget(QLabel("Metallic"))
        layout.addWidget(self.metallicSlider)

        # Roughness
        self.roughnessSlider = QSlider(Qt.Horizontal)
        self.roughnessSlider.setRange(0, 100)
        self.roughnessSlider.setValue(50)
        layout.addWidget(QLabel("Roughness"))
        layout.addWidget(self.roughnessSlider)

        # Specular
        self.specularSlider = QSlider(Qt.Horizontal)
        self.specularSlider.setRange(0, 100)
        self.specularSlider.setValue(10)
        layout.addWidget(QLabel("Specular"))
        layout.addWidget(self.specularSlider)

        # Specular Power
        self.specularPowerSlider = QSlider(Qt.Horizontal)
        self.specularPowerSlider.setRange(1, 128)
        self.specularPowerSlider.setValue(20)
        layout.addWidget(QLabel("Specular Power"))
        layout.addWidget(self.specularPowerSlider)

        # Base Color picker
        self.colorButton = QPushButton("Pick Base Color")
        layout.addWidget(self.colorButton)

        self.setLayout(layout)
