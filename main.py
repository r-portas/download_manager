# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Fri Jan  2 10:44:24 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.startButton = QtGui.QPushButton(self.centralwidget)
        self.startButton.setObjectName("startButton")
        self.gridLayout.addWidget(self.startButton, 0, 0, 1, 1)
        self.downloadsList = QtGui.QListWidget(self.centralwidget)
        self.downloadsList.setObjectName("downloadsList")
        self.gridLayout.addWidget(self.downloadsList, 0, 1, 3, 1)
        self.stopDownload = QtGui.QPushButton(self.centralwidget)
        self.stopDownload.setObjectName("stopDownload")
        self.gridLayout.addWidget(self.stopDownload, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Download = QtGui.QAction(MainWindow)
        self.actionNew_Download.setObjectName("actionNew_Download")
        self.menuFile.addAction(self.actionNew_Download)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Download Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.startButton.setText(QtGui.QApplication.translate("MainWindow", "Start Download", None, QtGui.QApplication.UnicodeUTF8))
        self.stopDownload.setText(QtGui.QApplication.translate("MainWindow", "Stop Download", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Download.setText(QtGui.QApplication.translate("MainWindow", "New Download", None, QtGui.QApplication.UnicodeUTF8))

