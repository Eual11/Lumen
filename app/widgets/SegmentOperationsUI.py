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
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.clearBtn = QToolButton(Form)
        self.clearBtn.setObjectName(u"clearBtn")
        self.clearBtn.setMinimumSize(QSize(64, 32))
        icon = QIcon()
        icon.addFile(u":/core/icons/icon-clear.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.clearBtn.setIcon(icon)
        self.clearBtn.setIconSize(QSize(28, 28))
        self.clearBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.clearBtn, 1, 3, 1, 5)

        self.smartRegionBtn = QToolButton(Form)
        self.smartRegionBtn.setObjectName(u"smartRegionBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smartRegionBtn.sizePolicy().hasHeightForWidth())
        self.smartRegionBtn.setSizePolicy(sizePolicy)
        self.smartRegionBtn.setMinimumSize(QSize(32, 32))
        icon1 = QIcon()
        icon1.addFile(u":/segmen-operation/icons/grow_region_connected.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.smartRegionBtn.setIcon(icon1)
        self.smartRegionBtn.setIconSize(QSize(28, 28))
        self.smartRegionBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.smartRegionBtn, 2, 0, 1, 2)

        self.selectBtn = QToolButton(Form)
        self.selectBtn.setObjectName(u"selectBtn")
        self.selectBtn.setMinimumSize(QSize(64, 32))
        icon2 = QIcon()
        icon2.addFile(u":/segmen-operation/icons/select.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.selectBtn.setIcon(icon2)
        self.selectBtn.setIconSize(QSize(28, 28))
        self.selectBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.selectBtn, 0, 0, 1, 1)

        self.eraseBtn = QToolButton(Form)
        self.eraseBtn.setObjectName(u"eraseBtn")
        self.eraseBtn.setMinimumSize(QSize(64, 32))
        icon3 = QIcon()
        icon3.addFile(u":/segmen-operation/icons/erase.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.eraseBtn.setIcon(icon3)
        self.eraseBtn.setIconSize(QSize(28, 28))
        self.eraseBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.eraseBtn, 0, 2, 1, 2)

        self.paintBtn = QToolButton(Form)
        self.paintBtn.setObjectName(u"paintBtn")
        self.paintBtn.setMinimumSize(QSize(64, 32))
        icon4 = QIcon()
        icon4.addFile(u":/segmen-operation/icons/paint.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.paintBtn.setIcon(icon4)
        self.paintBtn.setIconSize(QSize(28, 28))
        self.paintBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.paintBtn, 0, 1, 1, 1)

        self.fillHoles = QToolButton(Form)
        self.fillHoles.setObjectName(u"fillHoles")
        self.fillHoles.setMinimumSize(QSize(64, 32))
        icon5 = QIcon()
        icon5.addFile(u":/segmen-operation/icons/watershed.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.fillHoles.setIcon(icon5)
        self.fillHoles.setIconSize(QSize(28, 28))
        self.fillHoles.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.fillHoles, 1, 0, 1, 1)

        self.regionBtn = QToolButton(Form)
        self.regionBtn.setObjectName(u"regionBtn")
        sizePolicy.setHeightForWidth(self.regionBtn.sizePolicy().hasHeightForWidth())
        self.regionBtn.setSizePolicy(sizePolicy)
        self.regionBtn.setMinimumSize(QSize(32, 32))
        icon6 = QIcon()
        icon6.addFile(u":/segmen-operation/icons/grow_from_seed.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.regionBtn.setIcon(icon6)
        self.regionBtn.setIconSize(QSize(28, 28))
        self.regionBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.regionBtn, 1, 1, 1, 2)

        self.thresholdBtn = QToolButton(Form)
        self.thresholdBtn.setObjectName(u"thresholdBtn")
        self.thresholdBtn.setMinimumSize(QSize(64, 32))
        icon7 = QIcon()
        icon7.addFile(u":/segmen-operation/icons/threshold.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.thresholdBtn.setIcon(icon7)
        self.thresholdBtn.setIconSize(QSize(28, 28))
        self.thresholdBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.gridLayout.addWidget(self.thresholdBtn, 0, 4, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 97, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.clearBtn.setText(QCoreApplication.translate("Form", u"Clear", None))
        self.smartRegionBtn.setText(QCoreApplication.translate("Form", u"Smart Region Growing", None))
        self.selectBtn.setText(QCoreApplication.translate("Form", u"Select", None))
        self.eraseBtn.setText(QCoreApplication.translate("Form", u"Erase", None))
        self.paintBtn.setText(QCoreApplication.translate("Form", u"Paint", None))
        self.fillHoles.setText(QCoreApplication.translate("Form", u"Fill Holes", None))
        self.regionBtn.setText(QCoreApplication.translate("Form", u"Region Growing", None))
        self.thresholdBtn.setText(QCoreApplication.translate("Form", u"Threshold ", None))
    # retranslateUi

