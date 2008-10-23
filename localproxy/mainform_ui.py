# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainform.ui'
#
# Created: Thu Oct 23 09:49:59 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(400, 161)
        self.groupBox = QtGui.QGroupBox(MainForm)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 381, 111))
        self.groupBox.setObjectName("groupBox")
        self.proxyCheckBox = QtGui.QCheckBox(self.groupBox)
        self.proxyCheckBox.setGeometry(QtCore.QRect(10, 20, 90, 17))
        self.proxyCheckBox.setObjectName("proxyCheckBox")
        self.proxyEdit = QtGui.QLineEdit(self.groupBox)
        self.proxyEdit.setGeometry(QtCore.QRect(110, 20, 260, 20))
        self.proxyEdit.setObjectName("proxyEdit")
        self.fetchserverEdit = QtGui.QLineEdit(self.groupBox)
        self.fetchserverEdit.setGeometry(QtCore.QRect(110, 50, 260, 20))
        self.fetchserverEdit.setObjectName("fetchserverEdit")
        self.fetchserverCheckBox = QtGui.QCheckBox(self.groupBox)
        self.fetchserverCheckBox.setGeometry(QtCore.QRect(10, 50, 90, 17))
        self.fetchserverCheckBox.setObjectName("fetchserverCheckBox")
        self.applyButton = QtGui.QPushButton(self.groupBox)
        self.applyButton.setGeometry(QtCore.QRect(110, 80, 75, 23))
        self.applyButton.setObjectName("applyButton")
        self.saveButton = QtGui.QPushButton(self.groupBox)
        self.saveButton.setGeometry(QtCore.QRect(190, 80, 75, 23))
        self.saveButton.setObjectName("saveButton")
        self.hideButton = QtGui.QPushButton(MainForm)
        self.hideButton.setGeometry(QtCore.QRect(40, 130, 75, 23))
        self.hideButton.setObjectName("hideButton")
        self.upgradeButton = QtGui.QPushButton(MainForm)
        self.upgradeButton.setGeometry(QtCore.QRect(120, 130, 75, 23))
        self.upgradeButton.setObjectName("upgradeButton")
        self.aboutButton = QtGui.QPushButton(MainForm)
        self.aboutButton.setGeometry(QtCore.QRect(200, 130, 75, 23))
        self.aboutButton.setObjectName("aboutButton")
        self.quitButton = QtGui.QPushButton(MainForm)
        self.quitButton.setGeometry(QtCore.QRect(280, 130, 75, 23))
        self.quitButton.setObjectName("quitButton")

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        MainForm.setWindowTitle(QtGui.QApplication.translate("MainForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainForm", "GroupBox", None, QtGui.QApplication.UnicodeUTF8))
        self.proxyCheckBox.setText(QtGui.QApplication.translate("MainForm", "CheckBox", None, QtGui.QApplication.UnicodeUTF8))
        self.fetchserverCheckBox.setText(QtGui.QApplication.translate("MainForm", "CheckBox", None, QtGui.QApplication.UnicodeUTF8))
        self.applyButton.setText(QtGui.QApplication.translate("MainForm", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("MainForm", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.hideButton.setText(QtGui.QApplication.translate("MainForm", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.upgradeButton.setText(QtGui.QApplication.translate("MainForm", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutButton.setText(QtGui.QApplication.translate("MainForm", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.quitButton.setText(QtGui.QApplication.translate("MainForm", "PushButton", None, QtGui.QApplication.UnicodeUTF8))

