import sys
from PySide6.QtWidgets import QApplication, QLayout, QVBoxLayout, QWidget, QMainWindow
from PySide6 import QtCore
from app import LumenMainWindow,test
from app.widgets.DicomViewer import DicomViewer

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = LumenMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)


        self.view = DicomViewer("./res/dicom/vhm_head/")
        self.view2 = DicomViewer("./res/dicom/vhm_head/")

        self.ui.vtkContainer.addWidget(self.view)
        self.ui.vtkContainer.addWidget(self.view2)



        




def main():
    app = QApplication(sys.argv)

    ui = MainWindow()
    ui.show()
    ui.view.renderImage()
    sys.exit(app.exec())



if(__name__ == "__main__"):
    main()

