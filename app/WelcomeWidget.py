from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class WelcomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo = QLabel()
        pixmap = QPixmap(":core/icons/logo-full.svg")  # Use Qt resource path if available
        logo.setPixmap(pixmap.scaledToWidth(150, Qt.TransformationMode.SmoothTransformation))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title = QLabel("Lumen")
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtitle
        subtitle = QLabel("3D Reconstruction Tool for CT and MRI")
        subtitle.setStyleSheet("font-size: 16px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add widgets to layout
        layout.addWidget(logo)
        layout.addSpacing(20)
        layout.addWidget(title)
        layout.addWidget(subtitle)
