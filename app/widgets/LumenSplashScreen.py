
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QFont

class LumenSplashScreen(QWidget):
    def __init__(self, text: str = "Loading...", duration_ms: int = 2000):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAutoFillBackground(True)

        self.duration_ms = duration_ms
        self.setFixedSize(480, 200)

        # Main container layout (with margins and rounded background)
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(20, 20, 20, 20)
        outer_layout.setSpacing(0)

        # Inner horizontal layout
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)
        content_layout.setAlignment(Qt.AlignCenter)

        # Logo
        logo = QLabel()
        pixmap = QPixmap(":core/icons/logo-full.svg")
        logo.setPixmap(pixmap.scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)

        # Text
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("color: white;")
        text_label.setFont(QFont("Segoe UI", 20, QFont.Bold))

        # Add widgets to horizontal layout
        content_layout.addWidget(logo)
        content_layout.addWidget(text_label)

        # Add to outer layout
        outer_layout.addLayout(content_layout)
        self.setLayout(outer_layout)

        self.on_finish = None



    def show_for_duration(self, on_finish=None):
        self.show()
        self.on_finish = on_finish
        QTimer.singleShot(self.duration_ms, self.__finish)

    def __finish(self):
        self.close()
        if self.on_finish:
            self.on_finish()

