from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox,
    QDialogButtonBox, QFileDialog
)

class ExportActorDialog(QDialog):
    def __init__(self, lumen_core, parent=None):
        super().__init__(parent)
        self.lumen_core = lumen_core
        self.setWindowTitle("Export Selected Actor")

        # File format selection
        self.format_combo = QComboBox()
        self.format_combo.addItems(["OBJ", "STL"])

        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select export format:"))
        layout.addWidget(self.format_combo)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def accept(self):
        # Ask user for save path
        selected_format = self.format_combo.currentText()
        filters = "OBJ Files (*.obj)" if selected_format == "OBJ" else "STL Files (*.stl)"
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter(filters)
        if file_dialog.exec():
            filepath = file_dialog.selectedFiles()[0]
            self.export_actor(filepath, selected_format)

        return super().accept()

    def export_actor(self, filepath, selected_format):
        if not self.lumen_core.renderer.selected_actor:
            return

        if selected_format == "OBJ":
            self.lumen_core.renderer.write_selected_actor_obj(filepath)
        elif selected_format == "STL":
            self.lumen_core.renderer.write_selected_actor_stl(filepath)


def create_export_actor_dialog(lumen_core):
    selected_actor = lumen_core.renderer.selected_actor
    if not selected_actor:
        return

    dialog = ExportActorDialog(lumen_core)
    dialog.exec()
