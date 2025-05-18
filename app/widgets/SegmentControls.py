from PySide6.QtWidgets import QWidget
from .SegmentControlUI import Ui_segmentControl


class SegmentControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_segmentControl()
        self.ui.setupUi(self)

        self.add_segment_btn = self.ui.addSegmentBtn
        self.remove_segment_btn = self.ui.removeSegmentBtn
        self.render_btn = self.ui.renderBtn

