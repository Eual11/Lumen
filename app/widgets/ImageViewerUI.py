# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ImageViewerUI.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QSlider, QSpacerItem, QVBoxLayout, QWidget)

class Ui_ImageViewerUI(object):
    def setupUi(self, ImageViewerUI):
        if not ImageViewerUI.objectName():
            ImageViewerUI.setObjectName(u"ImageViewerUI")
        ImageViewerUI.resize(508, 452)
        self.verticalLayout_2 = QVBoxLayout(ImageViewerUI)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.imageInfo = QLabel(ImageViewerUI)
        self.imageInfo.setObjectName(u"imageInfo")

        self.horizontalLayout_10.addWidget(self.imageInfo)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_10)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.vtkParent = QWidget(ImageViewerUI)
        self.vtkParent.setObjectName(u"vtkParent")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.vtkParent.sizePolicy().hasHeightForWidth())
        self.vtkParent.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.vtkParent)

        self.sliceSlider = QSlider(ImageViewerUI)
        self.sliceSlider.setObjectName(u"sliceSlider")
        self.sliceSlider.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout.addWidget(self.sliceSlider)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_2)

        self.sliceIdxLabel = QLabel(ImageViewerUI)
        self.sliceIdxLabel.setObjectName(u"sliceIdxLabel")

        self.horizontalLayout_11.addWidget(self.sliceIdxLabel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_11)


        self.retranslateUi(ImageViewerUI)

        QMetaObject.connectSlotsByName(ImageViewerUI)
    # setupUi

    def retranslateUi(self, ImageViewerUI):
        ImageViewerUI.setWindowTitle(QCoreApplication.translate("ImageViewerUI", u"Form", None))
        self.imageInfo.setText("")
        self.sliceIdxLabel.setText(QCoreApplication.translate("ImageViewerUI", u"Slice:0/0", None))
    # retranslateUi

