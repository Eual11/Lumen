# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ActorControl.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_ActorControl(object):
    def setupUi(self, ActorControl):
        if not ActorControl.objectName():
            ActorControl.setObjectName(u"ActorControl")
        ActorControl.resize(400, 300)
        self.verticalLayout = QVBoxLayout(ActorControl)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.removeActorBtn = QPushButton(ActorControl)
        self.removeActorBtn.setObjectName(u"removeActorBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeActorBtn.sizePolicy().hasHeightForWidth())
        self.removeActorBtn.setSizePolicy(sizePolicy)
        self.removeActorBtn.setMinimumSize(QSize(72, 32))
        icon = QIcon()
        icon.addFile(u":/segment-control/minus-button.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.removeActorBtn.setIcon(icon)

        self.gridLayout.addWidget(self.removeActorBtn, 0, 0, 1, 1)

        self.exportActorBtn = QPushButton(ActorControl)
        self.exportActorBtn.setObjectName(u"exportActorBtn")
        self.exportActorBtn.setMinimumSize(QSize(64, 32))
        icon1 = QIcon()
        icon1.addFile(u":/segment-control/3d.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exportActorBtn.setIcon(icon1)

        self.gridLayout.addWidget(self.exportActorBtn, 0, 1, 1, 1)

        self.label = QLabel(ActorControl)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_2 = QLabel(ActorControl)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.surfaceComboBox = QComboBox(ActorControl)
        self.surfaceComboBox.addItem("")
        self.surfaceComboBox.addItem("")
        self.surfaceComboBox.addItem("")
        self.surfaceComboBox.setObjectName(u"surfaceComboBox")
        self.surfaceComboBox.setMinimumSize(QSize(29, 32))

        self.gridLayout.addWidget(self.surfaceComboBox, 2, 0, 1, 1)

        self.shadingComboBox = QComboBox(ActorControl)
        self.shadingComboBox.addItem("")
        self.shadingComboBox.addItem("")
        self.shadingComboBox.addItem("")
        self.shadingComboBox.addItem("")
        self.shadingComboBox.addItem("")
        self.shadingComboBox.setObjectName(u"shadingComboBox")
        self.shadingComboBox.setMinimumSize(QSize(0, 32))

        self.gridLayout.addWidget(self.shadingComboBox, 2, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(17, 179, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(ActorControl)

        QMetaObject.connectSlotsByName(ActorControl)
    # setupUi

    def retranslateUi(self, ActorControl):
        ActorControl.setWindowTitle(QCoreApplication.translate("ActorControl", u"Form", None))
        self.removeActorBtn.setText(QCoreApplication.translate("ActorControl", u"Remove", None))
        self.exportActorBtn.setText(QCoreApplication.translate("ActorControl", u"Export", None))
        self.label.setText(QCoreApplication.translate("ActorControl", u"Surface Style", None))
        self.label_2.setText(QCoreApplication.translate("ActorControl", u"Shading Style", None))
        self.surfaceComboBox.setItemText(0, QCoreApplication.translate("ActorControl", u"Surface ", None))
        self.surfaceComboBox.setItemText(1, QCoreApplication.translate("ActorControl", u"Point Cloud", None))
        self.surfaceComboBox.setItemText(2, QCoreApplication.translate("ActorControl", u"Wireframe", None))

        self.shadingComboBox.setItemText(0, QCoreApplication.translate("ActorControl", u"Phong", None))
        self.shadingComboBox.setItemText(1, QCoreApplication.translate("ActorControl", u"Blin-Phong", None))
        self.shadingComboBox.setItemText(2, QCoreApplication.translate("ActorControl", u"Flat", None))
        self.shadingComboBox.setItemText(3, QCoreApplication.translate("ActorControl", u"Gouraud", None))
        self.shadingComboBox.setItemText(4, QCoreApplication.translate("ActorControl", u"PBR", None))

    # retranslateUi

