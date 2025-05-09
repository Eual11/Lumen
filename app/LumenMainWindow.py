# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LumenMainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHBoxLayout,
    QLabel, QLayout, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1177, 733)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.label.setFont(font)

        self.horizontalLayout_2.addWidget(self.label)

        self.enableThr = QCheckBox(self.centralwidget)
        self.enableThr.setObjectName(u"enableThr")

        self.horizontalLayout_2.addWidget(self.enableThr)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.minThresholdSpinbox = QSpinBox(self.centralwidget)
        self.minThresholdSpinbox.setObjectName(u"minThresholdSpinbox")
        self.minThresholdSpinbox.setMinimum(-3000)
        self.minThresholdSpinbox.setMaximum(3000)

        self.horizontalLayout_2.addWidget(self.minThresholdSpinbox)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.maxThresholdSpinbox = QSpinBox(self.centralwidget)
        self.maxThresholdSpinbox.setObjectName(u"maxThresholdSpinbox")
        self.maxThresholdSpinbox.setMinimum(-3000)
        self.maxThresholdSpinbox.setMaximum(3000)
        self.maxThresholdSpinbox.setValue(40)

        self.horizontalLayout_2.addWidget(self.maxThresholdSpinbox)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.label_2.setFont(font1)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.rendererSelect = QComboBox(self.centralwidget)
        self.rendererSelect.addItem("")
        self.rendererSelect.addItem("")
        self.rendererSelect.addItem("")
        self.rendererSelect.addItem("")
        self.rendererSelect.setObjectName(u"rendererSelect")

        self.horizontalLayout_2.addWidget(self.rendererSelect)

        self.renderBtn = QPushButton(self.centralwidget)
        self.renderBtn.setObjectName(u"renderBtn")

        self.horizontalLayout_2.addWidget(self.renderBtn)

        self.loadBtn = QPushButton(self.centralwidget)
        self.loadBtn.setObjectName(u"loadBtn")

        self.horizontalLayout_2.addWidget(self.loadBtn)

        self.resetBtn = QPushButton(self.centralwidget)
        self.resetBtn.setObjectName(u"resetBtn")

        self.horizontalLayout_2.addWidget(self.resetBtn)

        self.saveObjBtn = QPushButton(self.centralwidget)
        self.saveObjBtn.setObjectName(u"saveObjBtn")

        self.horizontalLayout_2.addWidget(self.saveObjBtn)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.vtkContainer = QHBoxLayout()
        self.vtkContainer.setObjectName(u"vtkContainer")
        self.vtkContainer.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.vtkContainer.setContentsMargins(-1, -1, 8, -1)

        self.verticalLayout_3.addLayout(self.vtkContainer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Lumen", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Lumen", None))
        self.enableThr.setText(QCoreApplication.translate("MainWindow", u"Enable  Thresholding", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Min Thr", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Max Thr", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Renderer:", None))
        self.rendererSelect.setItemText(0, QCoreApplication.translate("MainWindow", u"Marching Cubes", None))
        self.rendererSelect.setItemText(1, QCoreApplication.translate("MainWindow", u"Flying Edges", None))
        self.rendererSelect.setItemText(2, QCoreApplication.translate("MainWindow", u"CPU volume raycasting", None))
        self.rendererSelect.setItemText(3, QCoreApplication.translate("MainWindow", u"GPU volume raycasting", None))

        self.renderBtn.setText(QCoreApplication.translate("MainWindow", u"Render", None))
        self.loadBtn.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.resetBtn.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.saveObjBtn.setText(QCoreApplication.translate("MainWindow", u"Save", None))
    # retranslateUi

