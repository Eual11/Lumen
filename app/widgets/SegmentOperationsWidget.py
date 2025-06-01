from PySide6.QtWidgets import QWidget
from .SegmentOperationsUI import Ui_Form


class SegmentOperationsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.selectBtn = self.ui.selectBtn
        self.paintBtn = self.ui.paintBtn
        self.eraseBtn = self.ui.eraseBtn
        self.watershedBtn = self.ui.watershedBtn
        self.regionBtn = self.ui.regionBtn
        self.smartRegionBtn = self.ui.smartRegionBtn


