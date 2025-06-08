# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ActorModifiersUI.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.decimateBtn = QToolButton(Form)
        self.decimateBtn.setObjectName(u"decimateBtn")
        self.decimateBtn.setMinimumSize(QSize(82, 64))
        icon = QIcon()
        icon.addFile(u":/core/icons/decimate_icon.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.decimateBtn.setIcon(icon)
        self.decimateBtn.setIconSize(QSize(28, 28))
        self.decimateBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.decimateBtn)

        self.clip = QToolButton(Form)
        self.clip.setObjectName(u"clip")
        self.clip.setMinimumSize(QSize(72, 64))
        icon1 = QIcon()
        icon1.addFile(u":/core/icons/clip.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.clip.setIcon(icon1)
        self.clip.setIconSize(QSize(28, 28))
        self.clip.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.clip)

        self.smoothBtn = QToolButton(Form)
        self.smoothBtn.setObjectName(u"smoothBtn")
        self.smoothBtn.setMinimumSize(QSize(72, 64))
        icon2 = QIcon()
        icon2.addFile(u":/core/icons/smoothing_icon.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.smoothBtn.setIcon(icon2)
        self.smoothBtn.setIconSize(QSize(28, 28))
        self.smoothBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.smoothBtn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.linearSubDivBtn = QToolButton(Form)
        self.linearSubDivBtn.setObjectName(u"linearSubDivBtn")
        self.linearSubDivBtn.setMinimumSize(QSize(129, 64))
        icon3 = QIcon()
        icon3.addFile(u":/core/icons/linear_subdiv.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.linearSubDivBtn.setIcon(icon3)
        self.linearSubDivBtn.setIconSize(QSize(28, 28))
        self.linearSubDivBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_2.addWidget(self.linearSubDivBtn)

        self.butterflySubDivBtn = QToolButton(Form)
        self.butterflySubDivBtn.setObjectName(u"butterflySubDivBtn")
        self.butterflySubDivBtn.setMinimumSize(QSize(129, 64))
        icon4 = QIcon()
        icon4.addFile(u":/core/icons/butter_fly.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.butterflySubDivBtn.setIcon(icon4)
        self.butterflySubDivBtn.setIconSize(QSize(28, 28))
        self.butterflySubDivBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_2.addWidget(self.butterflySubDivBtn)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 217, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.decimateBtn.setText(QCoreApplication.translate("Form", u"Decimate", None))
        self.clip.setText(QCoreApplication.translate("Form", u"Clip", None))
        self.smoothBtn.setText(QCoreApplication.translate("Form", u"Smooth", None))
        self.linearSubDivBtn.setText(QCoreApplication.translate("Form", u"Linear Subdivision", None))
        self.butterflySubDivBtn.setText(QCoreApplication.translate("Form", u"Butterfly Subdivision", None))
    # retranslateUi

