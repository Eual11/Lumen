# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SegmentOperations.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.selectBtn = QToolButton(Form)
        self.selectBtn.setObjectName(u"selectBtn")
        self.selectBtn.setMinimumSize(QSize(64, 32))
        icon = QIcon()
        icon.addFile(u":/segmen-operation/icons/select.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.selectBtn.setIcon(icon)
        self.selectBtn.setIconSize(QSize(28, 28))
        self.selectBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.selectBtn, 0, 0, 1, 1)

        self.paintBtn = QToolButton(Form)
        self.paintBtn.setObjectName(u"paintBtn")
        self.paintBtn.setMinimumSize(QSize(64, 32))
        icon1 = QIcon()
        icon1.addFile(u":/segmen-operation/icons/paint.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.paintBtn.setIcon(icon1)
        self.paintBtn.setIconSize(QSize(28, 28))
        self.paintBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.paintBtn, 0, 1, 1, 1)

        self.eraseBtn = QToolButton(Form)
        self.eraseBtn.setObjectName(u"eraseBtn")
        self.eraseBtn.setMinimumSize(QSize(64, 32))
        icon2 = QIcon()
        icon2.addFile(u":/segmen-operation/icons/erase.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.eraseBtn.setIcon(icon2)
        self.eraseBtn.setIconSize(QSize(28, 28))
        self.eraseBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.eraseBtn, 0, 2, 1, 1)

        self.thresholdBtn = QToolButton(Form)
        self.thresholdBtn.setObjectName(u"thresholdBtn")
        self.thresholdBtn.setMinimumSize(QSize(64, 32))
        icon3 = QIcon()
        icon3.addFile(u":/segmen-operation/icons/threshold.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.thresholdBtn.setIcon(icon3)
        self.thresholdBtn.setIconSize(QSize(28, 28))
        self.thresholdBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.thresholdBtn, 0, 3, 1, 1)

        self.watershedBtn = QToolButton(Form)
        self.watershedBtn.setObjectName(u"watershedBtn")
        self.watershedBtn.setMinimumSize(QSize(64, 32))
        icon4 = QIcon()
        icon4.addFile(u":/segmen-operation/icons/watershed.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.watershedBtn.setIcon(icon4)
        self.watershedBtn.setIconSize(QSize(28, 28))
        self.watershedBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.watershedBtn, 1, 0, 1, 1)

        self.regionBtn = QToolButton(Form)
        self.regionBtn.setObjectName(u"regionBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.regionBtn.sizePolicy().hasHeightForWidth())
        self.regionBtn.setSizePolicy(sizePolicy)
        self.regionBtn.setMinimumSize(QSize(32, 32))
        icon5 = QIcon()
        icon5.addFile(u":/segmen-operation/icons/grow_from_seed.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.regionBtn.setIcon(icon5)
        self.regionBtn.setIconSize(QSize(28, 28))
        self.regionBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.regionBtn, 1, 1, 1, 2)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.selectBtn.setText(QCoreApplication.translate("Form", u"Select", None))
        self.paintBtn.setText(QCoreApplication.translate("Form", u"Paint", None))
        self.eraseBtn.setText(QCoreApplication.translate("Form", u"Erase", None))
        self.thresholdBtn.setText(QCoreApplication.translate("Form", u"Threshold ", None))
        self.watershedBtn.setText(QCoreApplication.translate("Form", u"Watershed", None))
        self.regionBtn.setText(QCoreApplication.translate("Form", u"Region Growing", None))
    # retranslateUi

