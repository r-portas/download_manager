# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'popup.ui'
#
# Created: Thu Jan  8 07:02:04 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(458, 167)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.urlEdit = QtGui.QLineEdit(Dialog)
        self.urlEdit.setObjectName("urlEdit")
        self.gridLayout.addWidget(self.urlEdit, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.filenameEdit = QtGui.QLineEdit(Dialog)
        self.filenameEdit.setObjectName("filenameEdit")
        self.gridLayout.addWidget(self.filenameEdit, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.hashEdit = QtGui.QLineEdit(Dialog)
        self.hashEdit.setObjectName("hashEdit")
        self.gridLayout.addWidget(self.hashEdit, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 1)
        self.filepathDisplay = QtGui.QLabel(Dialog)
        self.filepathDisplay.setText("")
        self.filepathDisplay.setObjectName("filepathDisplay")
        self.gridLayout.addWidget(self.filepathDisplay, 3, 1, 1, 1)
        self.downloadPathButton = QtGui.QPushButton(Dialog)
        self.downloadPathButton.setObjectName("downloadPathButton")
        self.gridLayout.addWidget(self.downloadPathButton, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "New Download", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "URL", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Filename", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "MD5 Hash", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadPathButton.setText(QtGui.QApplication.translate("Dialog", "Select Path", None, QtGui.QApplication.UnicodeUTF8))

