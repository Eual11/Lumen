from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox,
    QDialogButtonBox, QFileDialog
)

class ExportRenderDialog(QDialog):
    def __init__(self, lumen_core, parent=None):
        super().__init__(parent)
        self.lumen_core = lumen_core
        self.setWindowTitle("Export Render")

        # File format selection
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "JPG"])

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
        filters = "PNG Files (*.png)" if selected_format == "PNG" else "JPEG Files (*.jpg)"
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter(filters)
        if file_dialog.exec():
            filepath = file_dialog.selectedFiles()[0]
            self.export_actor(filepath, selected_format)

        return super().accept()

    def export_actor(self, filepath, selected_format):
        if selected_format == "PNG":
            self.lumen_core.renderer.writePNG(filepath)
        elif selected_format == "JPG":
            self.lumen_core.renderer.writeJPG(filepath)


def create_export_render_dialog(lumen_core):

    dialog = ExportRenderDialog(lumen_core)

    dialog.exec()
 
