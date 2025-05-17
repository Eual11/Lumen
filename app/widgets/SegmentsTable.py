from PySide6.QtCore import QAbstractTableModel, QEvent, QItemSelection, QModelIndex, Qt
from PySide6.QtGui import QColor, QIcon, QMouseEvent, QPainter
from typing import List,Tuple

from PySide6.QtWidgets import QApplication, QColorDialog, QHeaderView, QStyledItemDelegate, QTableView, QVBoxLayout, QWidget
from core import Segment
class SegementTableModel(QAbstractTableModel):
    def __init__(self, data:List[Segment.Segment]):
        super().__init__()

        self._data_ref = data

        self._data = self.transform_to_internal(data)

        self.headers = ["Name", "Color", "Visibility"]

        self.segment_color_icon = QIcon("../../color-wheel.png")
        self.segment_visibility_icon = QIcon("../../eye.png")



    def transform_to_internal(self, data:List[Segment.Segment]):
        """
        Transforms given data model to internal representation. 
        currently to a 2D array
        """
        res =[]
        for segment in data:
            row = [segment.name, segment.color, segment.visibility,]
            res.append(row)


        return res

    def apply_changes(self)->None:

        """
        Registers changes on the table data model to the external data model we hold as a reference
        """

        for i in range(len(self._data)):

            row = self._data[i]

            self._data_ref[i].visibility = row[2]
            self._data_ref[i].color = row[1]
            self._data_ref[i].name = row[0]


    def rowCount(self, parent = QModelIndex()):
        return len(self._data)
    def columnCount(self, parent = QModelIndex()):
        return len(self._data[0]) if self._data else 0

    def data(self, index, role = Qt.DisplayRole):
        row, col = index.row(), index.column()

        if(role == Qt.DisplayRole and col !=1):
            return (self._data[row][col])

        if((role == Qt.BackgroundRole or role == Qt.EditRole) and col == 1):
            return QColor(*self._data[row][col])


        return None

    def flags(self, index):
        return Qt.ItemIsEditable| Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setData(self, index, value, role):
        row, col = index.row(), index.column()

        if col ==1 and role == Qt.EditRole and isinstance(value, tuple):
            self._data[row][col] = value[:3]
            self.apply_changes()
            return True

        if role == Qt.EditRole and col !=1:
            self._data[row][col] = value
            self.dataChanged.emit(index, index)
            self.apply_changes()
            return True
        return False

    def headerData(self, section: int, orientation: Qt.Orientation, /, role) :
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(section+1)
        if(role == Qt.DisplayRole and section ==0):
            if orientation == Qt.Horizontal :
                return self.headers[section]
        if role == Qt.ItemDataRole.DecorationRole and orientation == Qt.Horizontal:
            if section ==2:
                return self.segment_visibility_icon
            elif section ==1:
                return self.segment_color_icon
        return None

class SegementColorDelegate(QStyledItemDelegate):

    def createEditor(self, parent, option, index):

        color = index.model().data(index, role = Qt.EditRole)

        new_color = QColorDialog.getColor(initial=color, parent=parent, title="Select Color")

        if new_color.isValid():
           index.model().setData(index, new_color.toTuple(), role=Qt.EditRole)

    def paint(self,painter:QPainter, option, index):
        color = index.model().data(index, role = Qt.BackgroundRole )
        painter.save()
        painter.fillRect(option.rect, color)
        painter.restore()
class VisibilityDelegate(QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        return None
    def __init__(self, parent = None) -> None:
        super().__init__()

        # Loading display icons
        self.open_eye = QIcon("../../eye.png")
        self.close_eye = QIcon("../../hidden.png")

    def paint(self, painter:QPainter, option, index):

        visible = bool(index.model().data(index, Qt.DisplayRole))
        icon = self.open_eye if visible else self.close_eye


        icon_rect = option.rect.adjusted(6,6,-6,-6)

        painter.save()

        icon.paint(painter, icon_rect, Qt.AlignmentFlag.AlignCenter)



        painter.restore()

    def editorEvent(self, event:QEvent, model, option, index) ->bool:
        if not isinstance(event, QMouseEvent):
            return False
        if event.type() == QEvent.Type.MouseButtonRelease and  event.button() == Qt.MouseButton.LeftButton:
            current = bool(model.data(index, Qt.DisplayRole))
            model.setData(index, not current, role = Qt.EditRole)
            return True
        return False


class SegementsTableWidget(QWidget):
    def __init__(self, data, selection_callback=None, parent=None):
        super().__init__(parent)

        self.selection_callback = selection_callback
        self.data = data


        # Table Model

        self.model = SegementTableModel(self.data)

        self.view = QTableView()

        layout = QVBoxLayout()

        layout.addWidget(self.view)

        self.setLayout(layout)

        self.view.setModel(self.model)

        self.view.SelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.view.setStyleSheet("""
            QTableView::item:selected 
            {
                background-color: #095e7d;
            }
        """)

        self.view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.color_delegate = SegementColorDelegate()
        self.visibility_delegate = VisibilityDelegate()

        self.view.setItemDelegateForColumn(1,self.color_delegate)
        self.view.setItemDelegateForColumn(2,self.visibility_delegate)

        self.view.setColumnWidth(2,16)
        self.view.setColumnWidth(1,16)

        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def on_selection_changed(self, selected:QItemSelection, deselected:QItemSelection):
        if not self.selection_callback:
            return
       
        for index in selected.indexes():
            row = index.row()
            model = index.model()

            data = [model.index(row, col).data() for col in range(model.rowCount())]
            self.selection_callback(data)
            break

          
