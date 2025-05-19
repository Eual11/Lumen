# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LumenMainWindow2.0.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(822, 615)
        MainWindow.setMinimumSize(QSize(32, 32))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.toolbarHeader = QHBoxLayout()
        self.toolbarHeader.setObjectName(u"toolbarHeader")
        self.btnLoad = QPushButton(self.centralwidget)
        self.btnLoad.setObjectName(u"btnLoad")
        self.btnLoad.setMinimumSize(QSize(42, 32))
        self.btnLoad.setMaximumSize(QSize(42, 32))
        icon = QIcon()
        icon.addFile(u":/saveIcon/icons8-image-96.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnLoad.setIcon(icon)
        self.btnLoad.setIconSize(QSize(32, 32))

        self.toolbarHeader.addWidget(self.btnLoad)

        self.btnSaveRender = QPushButton(self.centralwidget)
        self.btnSaveRender.setObjectName(u"btnSaveRender")
        self.btnSaveRender.setMinimumSize(QSize(42, 32))
        self.btnSaveRender.setMaximumSize(QSize(42, 32))
        icon1 = QIcon()
        icon1.addFile(u":/newPrefix/icons8-save-100.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnSaveRender.setIcon(icon1)
        self.btnSaveRender.setIconSize(QSize(32, 32))

        self.toolbarHeader.addWidget(self.btnSaveRender)

        self.btnResetRenderer = QPushButton(self.centralwidget)
        self.btnResetRenderer.setObjectName(u"btnResetRenderer")
        self.btnResetRenderer.setMinimumSize(QSize(42, 32))
        self.btnResetRenderer.setMaximumSize(QSize(42, 32))
        icon2 = QIcon()
        icon2.addFile(u":/saveIcon/icons8-reset-50.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnResetRenderer.setIcon(icon2)
        self.btnResetRenderer.setIconSize(QSize(32, 32))

        self.toolbarHeader.addWidget(self.btnResetRenderer)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(85, 32))
        self.label_3.setScaledContents(True)

        self.toolbarHeader.addWidget(self.label_3)

        self.comboModules = QComboBox(self.centralwidget)
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AppointmentNew))
        self.comboModules.addItem(icon3, "")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AddressBookNew))
        self.comboModules.addItem(icon4, "")
        self.comboModules.addItem("")
        self.comboModules.addItem(icon3, "")
        self.comboModules.setObjectName(u"comboModules")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboModules.sizePolicy().hasHeightForWidth())
        self.comboModules.setSizePolicy(sizePolicy)
        self.comboModules.setMinimumSize(QSize(120, 0))
        self.comboModules.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)

        self.toolbarHeader.addWidget(self.comboModules)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.toolbarHeader.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.toolbarHeader)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.label_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.panelControls = QScrollArea(self.centralwidget)
        self.panelControls.setObjectName(u"panelControls")
        self.panelControls.setMinimumSize(QSize(360, 480))
        self.panelControls.setMaximumSize(QSize(320, 16777215))
        self.panelControls.setWidgetResizable(True)
        self.content = QWidget()
        self.content.setObjectName(u"content")
        self.content.setGeometry(QRect(0, 0, 358, 478))
        self.verticalLayout = QVBoxLayout(self.content)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.panelControls.setWidget(self.content)

        self.horizontalLayout.addWidget(self.panelControls)

        self.content_2 = QGridLayout()
        self.content_2.setObjectName(u"content_2")
        self.viewSecondary2 = QFrame(self.centralwidget)
        self.viewSecondary2.setObjectName(u"viewSecondary2")
        self.viewSecondary2.setFrameShape(QFrame.Shape.StyledPanel)
        self.viewSecondary2.setFrameShadow(QFrame.Shadow.Raised)

        self.content_2.addWidget(self.viewSecondary2, 1, 0, 1, 1)

        self.viewRender3D = QFrame(self.centralwidget)
        self.viewRender3D.setObjectName(u"viewRender3D")
        self.viewRender3D.setFrameShape(QFrame.Shape.StyledPanel)
        self.viewRender3D.setFrameShadow(QFrame.Shadow.Raised)

        self.content_2.addWidget(self.viewRender3D, 1, 1, 1, 1)

        self.viewPrimary = QFrame(self.centralwidget)
        self.viewPrimary.setObjectName(u"viewPrimary")
        self.viewPrimary.setFrameShape(QFrame.Shape.StyledPanel)
        self.viewPrimary.setFrameShadow(QFrame.Shadow.Raised)

        self.content_2.addWidget(self.viewPrimary, 0, 0, 1, 1)

        self.viewSecondary1 = QFrame(self.centralwidget)
        self.viewSecondary1.setObjectName(u"viewSecondary1")
        self.viewSecondary1.setFrameShape(QFrame.Shape.StyledPanel)
        self.viewSecondary1.setFrameShadow(QFrame.Shadow.Raised)

        self.content_2.addWidget(self.viewSecondary1, 0, 1, 1, 1)


        self.horizontalLayout.addLayout(self.content_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 822, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btnLoad.setText("")
        self.btnSaveRender.setText("")
        self.btnResetRenderer.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Modules", None))
        self.comboModules.setItemText(0, QCoreApplication.translate("MainWindow", u"Welcome to Lumen!", None))
        self.comboModules.setItemText(1, QCoreApplication.translate("MainWindow", u"Segementation", None))
        self.comboModules.setItemText(2, QCoreApplication.translate("MainWindow", u"Volume Rendering", None))
        self.comboModules.setItemText(3, QCoreApplication.translate("MainWindow", u"Surface Extraction", None))

        self.label_4.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

