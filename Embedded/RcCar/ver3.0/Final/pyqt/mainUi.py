# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainUi.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1004, 555)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.logText = QPlainTextEdit(self.centralwidget)
        self.logText.setObjectName(u"logText")
        self.logText.setGeometry(QRect(60, 50, 371, 291))
        font = QFont()
        font.setFamilies([u"Consolas"])
        self.logText.setFont(font)
        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setGeometry(QRect(770, 390, 91, 81))
        self.stopButton = QPushButton(self.centralwidget)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setGeometry(QRect(880, 390, 91, 81))
        self.goButton = QPushButton(self.centralwidget)
        self.goButton.setObjectName(u"goButton")
        self.goButton.setGeometry(QRect(150, 360, 81, 41))
        self.midButton = QPushButton(self.centralwidget)
        self.midButton.setObjectName(u"midButton")
        self.midButton.setGeometry(QRect(150, 410, 81, 41))
        self.rightButton = QPushButton(self.centralwidget)
        self.rightButton.setObjectName(u"rightButton")
        self.rightButton.setGeometry(QRect(240, 410, 81, 41))
        self.leftButton = QPushButton(self.centralwidget)
        self.leftButton.setObjectName(u"leftButton")
        self.leftButton.setGeometry(QRect(60, 410, 81, 41))
        self.backButton = QPushButton(self.centralwidget)
        self.backButton.setObjectName(u"backButton")
        self.backButton.setGeometry(QRect(150, 460, 81, 41))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 20, 161, 31))
        font1 = QFont()
        font1.setPointSize(12)
        self.label.setFont(font1)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(450, 20, 161, 31))
        self.label_2.setFont(font1)
        self.sensingText = QPlainTextEdit(self.centralwidget)
        self.sensingText.setObjectName(u"sensingText")
        self.sensingText.setGeometry(QRect(450, 50, 531, 291))
        self.sensingText.setFont(font)
        self.audoButton = QPushButton(self.centralwidget)
        self.audoButton.setObjectName(u"audoButton")
        self.audoButton.setGeometry(QRect(450, 390, 91, 81))
        self.ManualButton = QPushButton(self.centralwidget)
        self.ManualButton.setObjectName(u"ManualButton")
        self.ManualButton.setGeometry(QRect(580, 390, 91, 81))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1004, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.startButton.clicked.connect(MainWindow.start)
        self.goButton.clicked.connect(MainWindow.go)
        self.leftButton.clicked.connect(MainWindow.left)
        self.rightButton.clicked.connect(MainWindow.right)
        self.midButton.clicked.connect(MainWindow.mid)
        self.backButton.clicked.connect(MainWindow.back)
        self.stopButton.clicked.connect(MainWindow.stop)
        self.audoButton.clicked.connect(MainWindow.changeAuto)
        self.ManualButton.clicked.connect(MainWindow.changeManual)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.goButton.setText(QCoreApplication.translate("MainWindow", u"GO", None))
        self.midButton.setText(QCoreApplication.translate("MainWindow", u"MID", None))
        self.rightButton.setText(QCoreApplication.translate("MainWindow", u"RIGHT", None))
        self.leftButton.setText(QCoreApplication.translate("MainWindow", u"LEFT", None))
        self.backButton.setText(QCoreApplication.translate("MainWindow", u"BACK", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Command Table", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Sensing Table", None))
        self.audoButton.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.ManualButton.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
    # retranslateUi

