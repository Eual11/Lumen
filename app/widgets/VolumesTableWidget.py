from PySide6.QtCore import QAbstractTableModel, QEvent, QItemSelection, QModelIndex, Qt
from PySide6.QtGui import QColor, QIcon, QMouseEvent, QPainter
from typing import List,Tuple
from core import LumenCore
from PySide6.QtWidgets import QApplication, QColorDialog, QHeaderView, QStyledItemDelegate, QTableView, QVBoxLayout, QWidget

class VolumeTableModel(QAbstractTableModel):
    def __init__(self, data_owner: LumenCore.Lumen):
        super().__init__()
        self.data_owner = data_owner
        self.volume_dict = data_owner.renderer.volumes  # {vtkvolume: volumeInfo}
        self._data = list(self.volume_dict.items())  # list of (vtkVolume, volumeInfo)

        self.headers = ["Name", "Transform", "Visibility"]
        self.transform_icon = QIcon(":/core/icons/link_on")
        self.visibility_icon = QIcon(":/segment_table/eye.png")

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return 3

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        row, col = index.row(), index.column()
        volume, info = self._data[row]

        if role == Qt.DisplayRole:
            if col == 0:
                return getattr(info, "name", f"volume {row+1}")
            elif col == 1:
                return info['transform_enabled']
            elif col == 2:
                return info['visible'] 

        return None

    def setData(self, index, value, role):
        row, col = index.row(), index.column()
        volume, info = self._data[row]

        if role == Qt.EditRole:
            if col == 0:
                info['name'] = value
                self.dataChanged.emit(index, index)
                return True
            elif col == 1:
                info['transform_enabled'] = value
                self.data_owner.renderer.set_volume_transform(volume, value)
                self.dataChanged.emit(index, index)
                return True
            elif col == 2:
                info['visible'] = value
                self.data_owner.renderer.set_volume_visibility(volume, value)
                self.dataChanged.emit(index, index)
                return True

        return False

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole and section ==0:
                return self.headers[section]
            elif role == Qt.DecorationRole:
                if section == 1:
                    return self.transform_icon
                elif section == 2:
                    return self.visibility_icon
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(section + 1)
        return None

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def update_model(self):
        self._data = list(self.volume_dict.items())
        self.layoutChanged.emit()



class ToggleDelegate(QStyledItemDelegate):
    def __init__(self, icon_on: QIcon, icon_off: QIcon, parent=None):
        super().__init__(parent)
        self.icon_on = icon_on
        self.icon_off = icon_off
    def createEditor(self, parent, option, index):
        return None

    def paint(self, painter, option, index):
        value = bool(index.model().data(index, Qt.DisplayRole))
        icon = self.icon_on if value else self.icon_off
        icon_rect = option.rect.adjusted(6, 6, -6, -6)
        painter.save()
        icon.paint(painter, icon_rect, Qt.AlignCenter)
        painter.restore()

    def editorEvent(self, event: QEvent, model, option, index):
        if not isinstance(event, QMouseEvent):
            return False
        if event.type() == QEvent.Type.MouseButtonRelease and event.button() == Qt.LeftButton:
            current = bool(model.data(index, Qt.DisplayRole))
            model.setData(index, not current, role=Qt.EditRole)
            return True
        return False


class VolumesTableWidget(QWidget):
    def __init__(self, data_owner, selection_callback=None, parent=None):
        super().__init__(parent)

        self.selection_callback = selection_callback
        self.data_owner = data_owner

        # Table Model
        self.model = VolumeTableModel( self.data_owner)
        self.view = QTableView()
        self.view.setModel(self.model)

        # View Styling
        self.view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.view.setStyleSheet("""
        QTableView::item:selected {
            background-color: #095e7d;
        }
        QTableView {
            border: 2px solid #444;
            gridline-color: #ccc;
        }
        """)

        # Delegates
        transform_on_icon = QIcon(":/core/icons/link_on.svg")
        transform_off_icon = QIcon(":/core/icons/link_off.svg")

        visibility_on_icon = QIcon(":/segment_table/eye.png")
        visibility_off_icon = QIcon(":/segment_table/hidden.png")

        self.transform_delegate = ToggleDelegate(
        icon_on=transform_on_icon,
        icon_off=transform_off_icon,
        )

        self.visibility_delegate = ToggleDelegate(
        icon_on=visibility_on_icon,
        icon_off=visibility_off_icon,
        )
        self.view.setItemDelegateForColumn(1, self.transform_delegate)
        self.view.setItemDelegateForColumn(2, self.visibility_delegate)
        self.view.setColumnWidth(1, 16)
        self.view.setColumnWidth(2, 16)

        # Resize behavior
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.view.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        # Selection callback
        self.view.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        if self.selection_callback:
            indexes = selected.indexes()
            if indexes:
                row = indexes[0].row()
                volume, info = self.model._data[row]
                self.selection_callback(volume, info)
            else:
                self.selection_callback(None, None)

    def set_selection_change_callback(self, callback):
        self.selection_callback = callback
        self.view.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def update_model(self):
        self.model.update_model()

