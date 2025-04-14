import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QFileDialog
from PySide6 import QtCore
from app import LumenMainWindow,test
from app.widgets.DicomViewer import DicomViewer

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = LumenMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)


        self.view = DicomViewer()
        self.view2 = DicomViewer()

        self.ui.vtkContainer.addWidget(self.view)
        self.ui.vtkContainer.addWidget(self.view2)


        #NOTE: testing buttons and loading


        self.ui.loadBtn.clicked.connect(lambda: self.load(0))
        self.ui.renderBtn.clicked.connect(lambda: self.load(1))

    def closeEvent(self, event) -> None:
        self.view.cleanup()
        self.view2.cleanup()
        return super().closeEvent(event)

    @QtCore.Slot()
    def load(self, n):
        dir = QFileDialog.getExistingDirectory(None, "Select Dicom Folder")

        if(dir and n==0):
            self.view.loadImage(dir)
        if(dir and n==1):
            self.view2.loadImage(dir)







        




def main():
    app = QApplication(sys.argv)

    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())



if(__name__ == "__main__"):
    main()

