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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ActorControl(object):
    def setupUi(self, ActorControl):
        if not ActorControl.objectName():
            ActorControl.setObjectName(u"ActorControl")
        ActorControl.resize(400, 300)
        self.verticalLayout = QVBoxLayout(ActorControl)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.content = QHBoxLayout()
        self.content.setObjectName(u"content")
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

        self.content.addWidget(self.removeActorBtn)

        self.exportActorBtn = QPushButton(ActorControl)
        self.exportActorBtn.setObjectName(u"exportActorBtn")
        self.exportActorBtn.setMinimumSize(QSize(64, 32))
        icon1 = QIcon()
        icon1.addFile(u":/segment-control/3d.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exportActorBtn.setIcon(icon1)

        self.content.addWidget(self.exportActorBtn)


        self.verticalLayout.addLayout(self.content)

        self.verticalSpacer = QSpacerItem(20, 239, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(ActorControl)

        QMetaObject.connectSlotsByName(ActorControl)
    # setupUi

    def retranslateUi(self, ActorControl):
        ActorControl.setWindowTitle(QCoreApplication.translate("ActorControl", u"Form", None))
        self.removeActorBtn.setText(QCoreApplication.translate("ActorControl", u"Remove", None))
        self.exportActorBtn.setText(QCoreApplication.translate("ActorControl", u"Export", None))
    # retranslateUi

