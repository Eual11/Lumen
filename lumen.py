from typing import Optional
from PySide6 import QtCore
from PySide6.QtGui import Qt
from PySide6.QtCharts import QBarSet, QBarSeries, QChart, QChartView, QValueAxis
from PySide6.QtWidgets import QApplication, QDoubleSpinBox, QFileDialog, QLabel, QLayout, QMainWindow, QSlider, QVBoxLayout, QFileDialog, QWidget
from app.HistogramWidget import HistogramWidget
from app.LumenMainWindow2 import Ui_MainWindow
from app.WelcomeWidget import WelcomeWidget
from app.widgets import SegmentControls, SegmentOperationsWidget, SegmentsTable
from app.widgets.DicomViewer import ViewerMode
import app.widgets.RCS_rc

import sys
from app.widgets.RegionGrowingDialog import create_region_grow_dialog
from app.widgets.SmartRegionGrowingDialog import create_smart_region_grow_dialog
from app.widgets.ThresholdDialog import ThresholdDialog, create_threshold_dialog
from core.LumenCore import Lumen, RenderMethods
from core.SegmentOperationCommand import RegionGrowCommand
class LumenMainWindow(QMainWindow):
    def __init__(self)->None:
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Lumen")

        self.welcome_widget = WelcomeWidget()

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

        self.segments_table = SegmentsTable.SegementsTableWidget(self.lumen_core.segments,self.lumen_core)

        # Dialogs 

        self.threshold_dialog = ThresholdDialog(None)


        # SidePanel UI

        self.ui.comboModules.currentIndexChanged.connect(self.load_sidebar_ui)



        # Lumen Welcome Screen
        self.load_welcome_widget()








        

    @QtCore.Slot()
    def resetRenderer(self):
        self.lumen_core.reset_renderer()
    @QtCore.Slot()
    def load(self):
        dir = QFileDialog.getExistingDirectory(None, "Load Dicom Image")
        self.lumen_core.load_image(dir)
        self.segments_table.update_model()

    @QtCore.Slot()
    def render(self):
        method = self.segment_control.reconMethod.currentIndex()
        if method == 0:
            self.lumen_core.render_selected_segment(RenderMethods.MARCHING_CUBES)
        elif method == 1:
            self.lumen_core.render_selected_segment(RenderMethods.FLYING_EDGES)
        elif method == 2:
            self.lumen_core.render_selected_segment(RenderMethods.CPU_RAYCASTING)
        elif method == 3:
            self.lumen_core.render_selected_segment(RenderMethods.GPU_RAYCASTING)



    def closeEvent(self, event)->None:
        self.lumen_core.cleanup()
        return super().closeEvent(event)
    def addSegment(self):
        self.lumen_core.create_segement(color=(255,1,1))
        self.segments_table.update_model()
    def removeSegment(self):
       self.lumen_core.delete_selected_segment()
       self.segments_table.update_model()
    @QtCore.Slot()
    def segment_table_selection_change(self, selected:QtCore.QItemSelection, deselected:QtCore.QItemSelection):
        if not len(selected.indexes()):
            self.lumen_core.set_selected_segment(-1)
        else:
            row = selected.indexes()[0].row()
            self.lumen_core.set_selected_segment(row)
    def disconnect_signals(self, widget:QWidget):
        for sig in getattr(widget, "_connected_signals",[]):
            try:
                print(sig)
                sig.disconnect()
            except:
                pass

    def clear_layout(self, layout:Optional[QLayout]):
        if not layout:
            return

        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()

            if widget:
                self.disconnect_signals(widget)
                widget.setParent(None)
            else:
                layout = widget.layout()
                self.clear_layout(layout)

    def load_segment_editor(self):

        #TODO: clear layout first
        # Segment Editor Layout
        self.clear_layout(self.ui.content.layout())
        layout = self.ui.content.layout()

        self.segment_control = SegmentControls.SegmentControls()
        self.segment_operations = SegmentOperationsWidget.SegmentOperationsWidget()


        # Segment Operations
        self.segment_operations.ui.thresholdBtn.clicked.connect(lambda:create_threshold_dialog(self.lumen_core))
        self.segment_operations.ui.paintBtn.clicked.connect(lambda: self.lumen_core.viewer.set_viewer_mode(ViewerMode.PAINT))
        self.segment_operations.ui.eraseBtn.clicked.connect(lambda: self.lumen_core.viewer.set_viewer_mode(ViewerMode.ERASE))
        self.segment_operations.ui.regionBtn.clicked.connect(lambda: create_region_grow_dialog(self.lumen_core))
        self.segment_operations.ui.smartRegionBtn.clicked.connect(lambda:create_smart_region_grow_dialog(self.lumen_core))




        self.segments_table.set_selection_change_callback(self.segment_table_selection_change)
        self.segments_table.setMinimumHeight(320)
        self.segment_operations.setMinimumHeight(220)


        num_samples = 1000
        img_min,img_max = self.lumen_core.get_image_range()


        bins = self.lumen_core.get_image_histogram(20,num_samples)
        hist = HistogramWidget("Image Histogram", bins, img_min, 0, img_max/2, num_samples)
        hist.setFixedHeight(280)
        
       



        self.ui.content.layout().addWidget(self.segment_control)
        self.ui.content.layout().addWidget(QLabel("Segments"))
        self.ui.content.layout().addWidget(self.segments_table)
        self.ui.content.layout().addWidget(QLabel("Segment Operations"))
        self.ui.content.layout().addWidget(self.segment_operations)
        slider = QDoubleSpinBox()
        slider.setSingleStep(1)
        slider.setValue(1)
        slider.valueChanged.connect(lambda x: self.lumen_core.set_isovalue(x))

        layout.addWidget(QLabel("Segment Isovalue"))
        layout.addWidget(slider)
        layout.addWidget(hist)

        self.segment_control.add_segment_btn.clicked.connect(self.addSegment)
        self.segment_control.remove_segment_btn.clicked.connect(self.removeSegment)

        self.segment_control.render_btn.clicked.connect(self.render)
    def load_welcome_widget(self):
        self.clear_layout(self.ui.content.layout())

        self.ui.content.layout().addWidget(self.welcome_widget)
    def test_region_growing(self):
        self.lumen_core.viewer.set_viewer_mode(ViewerMode.SEED_PLACEMENT)

        segment = self.lumen_core.get_selected_segment()
        if segment:
            cmd = RegionGrowCommand(self.lumen_core.get_pipeline_output_data(), segment, 300,2000,[])
            self.lumen_core.viewer.seed_placement_command = cmd
    def load_sidebar_ui(self, idx:int):
        if idx==0:
            self.load_welcome_widget()
        elif idx==1:
            self.load_segment_editor()
        elif idx ==2:
            self.load_surface_recon_module()
    def load_surface_recon_module(self):
        self.clear_layout(self.ui.content.layout())

        layout = self.ui.content.layout()

        
       
        
        






if __name__ == "__main__":

    app = QApplication([])

    lumen = LumenMainWindow()
    lumen.showMaximized()
    lumen.show()
    sys.exit(app.exec())
