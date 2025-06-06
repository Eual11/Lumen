from PySide6.QtWidgets import QWidget

from app.widgets.ActorControlUI import Ui_ActorControl


class ActorControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_ActorControl()
        self.ui.setupUi(self)

        self.remove_actor_btn = self.ui.removeActorBtn
        self.export_btn = self.ui.exportActorBtn


