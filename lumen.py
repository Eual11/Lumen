from PySide6 import QtCore
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QApplication, QFileDialog, QLabel, QMainWindow, QVBoxLayout, QFileDialog
from app.LumenMainWindow2 import Ui_MainWindow
from app.widgets import SegmentControls, SegmentsTable
import sys

from core.LumenCore import Lumen
class LumenMainWindow(QMainWindow):
    def __init__(self)->None:
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Core Lumen Internals object
        self.lumen_core = Lumen()

        self.view = self.lumen_core.get_viewer()
        self.renderer = self.lumen_core.get_renderer()


        # Setting up UI for VTK Image viewers and Renderer

        l1 = QVBoxLayout()
        l1.addWidget(self.view)

        l2 = QVBoxLayout()
        l2.addWidget(self.renderer)

        self.ui.viewPrimary.setLayout(l1)
        self.ui.viewSecondary1.setLayout(l2)

        self.ui.btnLoad.clicked.connect(self.load)
        self.ui.btnResetRenderer.clicked.connect(self.resetRenderer)


        # SidePanel UI

        self.segment_control = SegmentControls.SegmentControls()
        self.lumen_core.create_segement("Segment 1", (1,1,1))
        self.segments_table = SegmentsTable.SegementsTableWidget(self.lumen_core.segments)
        self.segments_table.set_selection_change_callback(self.on_segment_table_selection_change)




        self.ui.content.layout().addWidget(self.segment_control)
        self.ui.content.layout().addWidget(self.segments_table)

        self.segment_control.add_segment_btn.clicked.connect(self.addSegment)
        self.segment_control.remove_segment_btn.clicked.connect(self.removeSegment)



    @QtCore.Slot()
    def resetRenderer(self):
        self.lumen_core.reset_renderer()
    @QtCore.Slot()
    def load(self):
        dir = QFileDialog.getExistingDirectory(None, "Load Dicom Image")
        self.lumen_core.load_image(dir)

    def closeEvent(self, event)->None:
        self.lumen_core.cleanup()
        return super().closeEvent(event)
    def addSegment(self):
        self.lumen_core.create_segement("Segment 1", (1,1,1))
        self.segments_table.update_model()
    def removeSegment(self):
       self.lumen_core.delete_selected_segment()
       self.segments_table.update_model()
    @QtCore.Slot()
    def on_segment_table_selection_change(self, selected:QtCore.QItemSelection, deselected:QtCore.QItemSelection):
        if not len(selected.indexes()):
            self.lumen_core.selected_segment = -1
        row = selected.indexes()[0].row()
        self.lumen_core.selected_segment = row
        
        
        






if __name__ == "__main__":

    app = QApplication([])
    lumen = LumenMainWindow()

    lumen.show()
    sys.exit(app.exec())
