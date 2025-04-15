import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QFileDialog
from PySide6 import QtCore
from app import LumenMainWindow
from app.widgets import Renderer
from app.widgets.DicomViewer import DicomViewer

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from core import DicomLoader
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = LumenMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.loader = DicomLoader.DicomLoader()


        self.view = DicomViewer(self.loader.get_output_port())
        self.renderer = Renderer.Renderer()

        self.ui.vtkContainer.addWidget(self.view)
        self.ui.vtkContainer.addWidget(self.renderer)


        #NOTE: testing buttons and loading


        self.ui.loadBtn.clicked.connect(lambda: self.load(0))

    def closeEvent(self, event) -> None:
        self.view.cleanup()
        self.renderer.cleanup()
        return super().closeEvent(event)

    @QtCore.Slot()
    def load(self, n):
        dir = QFileDialog.getExistingDirectory(None, "Select Dicom Folder")

        if(dir and n==0):
            self.loader.load_imge(dir)
            self.view.updateSource(self.loader.get_output_port())
    

def main():
    app = QApplication(sys.argv)

    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())



if(__name__ == "__main__"):
    main()

