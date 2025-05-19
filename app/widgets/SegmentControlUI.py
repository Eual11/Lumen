# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SegmentControl.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_segmentControl(object):
    def setupUi(self, segmentControl):
        if not segmentControl.objectName():
            segmentControl.setObjectName(u"segmentControl")
        segmentControl.resize(400, 300)
        self.verticalLayout = QVBoxLayout(segmentControl)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.content = QHBoxLayout()
        self.content.setObjectName(u"content")
        self.addSegmentBtn = QPushButton(segmentControl)
        self.addSegmentBtn.setObjectName(u"addSegmentBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addSegmentBtn.sizePolicy().hasHeightForWidth())
        self.addSegmentBtn.setSizePolicy(sizePolicy)
        self.addSegmentBtn.setMinimumSize(QSize(64, 32))
        icon = QIcon()
        icon.addFile(u":/segment-control/plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.addSegmentBtn.setIcon(icon)

        self.content.addWidget(self.addSegmentBtn)

        self.removeSegmentBtn = QPushButton(segmentControl)
        self.removeSegmentBtn.setObjectName(u"removeSegmentBtn")
        sizePolicy.setHeightForWidth(self.removeSegmentBtn.sizePolicy().hasHeightForWidth())
        self.removeSegmentBtn.setSizePolicy(sizePolicy)
        self.removeSegmentBtn.setMinimumSize(QSize(72, 32))
        icon1 = QIcon()
        icon1.addFile(u":/segment-control/minus-button.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.removeSegmentBtn.setIcon(icon1)

        self.content.addWidget(self.removeSegmentBtn)

        self.renderBtn = QPushButton(segmentControl)
        self.renderBtn.setObjectName(u"renderBtn")
        self.renderBtn.setMinimumSize(QSize(64, 32))
        icon2 = QIcon()
        icon2.addFile(u":/segment-control/3d.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.renderBtn.setIcon(icon2)

        self.content.addWidget(self.renderBtn)

        self.reconMethod = QComboBox(segmentControl)
        self.reconMethod.addItem("")
        self.reconMethod.addItem("")
        self.reconMethod.addItem("")
        self.reconMethod.addItem("")
        self.reconMethod.addItem("")
        self.reconMethod.setObjectName(u"reconMethod")
        sizePolicy.setHeightForWidth(self.reconMethod.sizePolicy().hasHeightForWidth())
        self.reconMethod.setSizePolicy(sizePolicy)
        self.reconMethod.setMinimumSize(QSize(64, 32))

        self.content.addWidget(self.reconMethod)


        self.verticalLayout.addLayout(self.content)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(segmentControl)

        QMetaObject.connectSlotsByName(segmentControl)
    # setupUi

    def retranslateUi(self, segmentControl):
        segmentControl.setWindowTitle(QCoreApplication.translate("segmentControl", u"Form", None))
        self.addSegmentBtn.setText(QCoreApplication.translate("segmentControl", u"Add", None))
        self.removeSegmentBtn.setText(QCoreApplication.translate("segmentControl", u"Remove", None))
        self.renderBtn.setText(QCoreApplication.translate("segmentControl", u"Render", None))
        self.reconMethod.setItemText(0, QCoreApplication.translate("segmentControl", u"Marching Cubes", None))
        self.reconMethod.setItemText(1, QCoreApplication.translate("segmentControl", u"Flying Edges", None))
        self.reconMethod.setItemText(2, QCoreApplication.translate("segmentControl", u"New Item", None))
        self.reconMethod.setItemText(3, QCoreApplication.translate("segmentControl", u"CPU Volume RayCasting", None))
        self.reconMethod.setItemText(4, QCoreApplication.translate("segmentControl", u"GPU Volume RayCasting", None))

    # retranslateUi

