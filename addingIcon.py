
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QIcon

app = QApplication([])

table = QTableWidget(3, 2)
table.setAlternatingRowColors(True)

item_with_icon = QTableWidgetItem("Label with icon")
item_with_icon.setIcon(QIcon("icon.png"))  # path to your icon
table.setItem(0, 0, item_with_icon)

table.setItem(1, 0, QTableWidgetItem("Regular Row"))
table.setItem(2, 0, QTableWidgetItem("Another Row"))
table.resize(400, 200)
table.show()

app.exec()
