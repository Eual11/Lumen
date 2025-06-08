from PySide6.QtWidgets import QWidget
from app.widgets.ActorModifiersUI import Ui_Form


class ActorModifiersWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.decimateBtn = self.ui.decimateBtn
        self.smoothBtn = self.ui.smoothBtn
        self.clipBtn = self.ui.clip
        self.butterflySubDiv = self.ui.butterflySubDivBtn
        self.linearSubDiv = self.ui.linearSubDivBtn



