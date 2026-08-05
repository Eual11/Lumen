from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QFileDialog, QDialogButtonBox, QSpinBox, QDoubleSpinBox, QWidget,
    QApplication, QMessageBox
)
from PySide6.QtCore import Qt
from core.LumenCore import Lumen
from vtkmodules.vtkImagingGeneral import vtkImageGaussianSmooth, vtkImageGradientMagnitude, vtkImageLaplacian, vtkImageMedian3D

class DicomLoadDialog(QDialog):
    def __init__(self, lumen_core: Lumen, segments_table, parent=None):
        super().__init__(parent)
        self.lumen_core = lumen_core
        self.segments_table = segments_table
        self.setWindowTitle("Load DICOM Image with Filter")

        self.selected_dir = None

        self.dir_label = QLabel("No folder selected")
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.select_directory)
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.dir_label)
        dir_layout.addWidget(self.browse_button)

        # A DICOM folder often holds several acquisitions with different matrix
        # sizes, so one has to be picked rather than stacked together.
        self.series_combo = QComboBox()
        self.series_combo.setEnabled(False)
        self.series_combo.addItem("Select a folder first", None)
        series_layout = QHBoxLayout()
        series_layout.addWidget(QLabel("Series:"))
        series_layout.addWidget(self.series_combo, 1)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["None", "Median", "Gaussian", "Laplacian", "Gradient"])
        self.filter_combo.currentIndexChanged.connect(self.update_filter_params_ui)
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Apply Filter:"))
        filter_layout.addWidget(self.filter_combo)

        self.params_widget = QWidget()
        self.params_layout = QVBoxLayout()
        self.params_widget.setLayout(self.params_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(dir_layout)
        main_layout.addLayout(series_layout)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.params_widget)
        main_layout.addWidget(self.button_box)
        self.setLayout(main_layout)

        self.param_controls = {}
        self.update_filter_params_ui(0)

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select DICOM Directory")
        if dir_path:
            self.selected_dir = dir_path
            self.dir_label.setText(dir_path)
            self.populate_series(dir_path)

    def populate_series(self, dir_path):
        self.series_combo.clear()

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            series = self.lumen_core.scan_dicom_series(dir_path)
        finally:
            QApplication.restoreOverrideCursor()

        if not series:
            self.series_combo.addItem("No DICOM series found", None)
            self.series_combo.setEnabled(False)
            return

        for s in series:
            self.series_combo.addItem(s.label(), s.uid)
        self.series_combo.setEnabled(len(series) > 1)

    def clear_params_ui(self):
        for i in reversed(range(self.params_layout.count())):
            widget = self.params_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.param_controls = {}

    def update_filter_params_ui(self, index):
        self.clear_params_ui()

        if index == 1:  # Median
            spin = QSpinBox()
            spin.setRange(1, 9)
            spin.setValue(3)
            self.params_layout.addWidget(QLabel("Kernel Size:"))
            self.params_layout.addWidget(spin)
            self.param_controls["kernel"] = spin

        elif index == 2:  # Gaussian
            std_spin = QDoubleSpinBox()
            std_spin.setRange(0.1, 10.0)
            std_spin.setSingleStep(0.1)
            std_spin.setValue(2.0)

            self.params_layout.addWidget(QLabel("Standard Deviation (all dims):"))
            self.params_layout.addWidget(std_spin)
            self.param_controls["stddev"] = std_spin

        elif index in (3, 4):  # Laplacian or Gradient — no parameters, just note
            self.params_layout.addWidget(QLabel("No configurable parameters."))

    def accept(self):
        if not self.selected_dir:
            return

        series_uid = self.series_combo.currentData()

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            loaded = self.lumen_core.load_image(self.selected_dir, series_uid)
        finally:
            QApplication.restoreOverrideCursor()

        if not loaded:
            QMessageBox.critical(
                self,
                "Load Failed",
                "Could not load a DICOM volume from:\n"
                f"{self.selected_dir}\n\n"
                "The folder may contain no readable DICOM series, or the files "
                "may use an unsupported format. See the console for details.",
            )
            return

        current_filter = self.filter_combo.currentIndex()

        if current_filter == 1:  # Median
            kernel = self.param_controls["kernel"].value()
            median_filter = vtkImageMedian3D()
            median_filter.SetKernelSize(kernel, kernel, kernel)
            self.lumen_core.add_filter(median_filter)

        elif current_filter == 2:  # Gaussian
            stddev = self.param_controls["stddev"].value()
            gaussian_filter = vtkImageGaussianSmooth()
            gaussian_filter.SetDimensionality(3)
            gaussian_filter.SetRadiusFactors(stddev, stddev, stddev)
            gaussian_filter.SetStandardDeviations(stddev, stddev, stddev)
            self.lumen_core.add_filter(gaussian_filter)

        elif current_filter == 3:  # Laplacian
            laplacian_filter = vtkImageLaplacian()
            self.lumen_core.add_filter(laplacian_filter)

        elif current_filter == 4:  # Gradient
            gradient_filter = vtkImageGradientMagnitude()
            gradient_filter.SetDimensionality(3)
            self.lumen_core.add_filter(gradient_filter)

        self.lumen_core.update_viewer()
        self.segments_table.update_model()
        super().accept()


def create_load_dicom_dialog(lumen_core: Lumen, segments_table):
    dialog = DicomLoadDialog(lumen_core, segments_table)
    dialog.exec()

