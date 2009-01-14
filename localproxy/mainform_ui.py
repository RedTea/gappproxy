# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainform.ui'
#
# Created: Wed Jan 14 18:15:40 2009
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
        self.proxyCheckBox.setGeometry(QtCore.QRect(10, 20, 120, 17))
        self.proxyCheckBox.setCheckable(True)
        self.proxyCheckBox.setObjectName("proxyCheckBox")
        self.proxyEdit = QtGui.QLineEdit(self.groupBox)
        self.proxyEdit.setEnabled(False)
        self.proxyEdit.setGeometry(QtCore.QRect(130, 20, 240, 20))
        self.proxyEdit.setObjectName("proxyEdit")
        self.fetchserverEdit = QtGui.QLineEdit(self.groupBox)
        self.fetchserverEdit.setEnabled(False)
        self.fetchserverEdit.setGeometry(QtCore.QRect(130, 50, 240, 20))
        self.fetchserverEdit.setObjectName("fetchserverEdit")
        self.fetchserverCheckBox = QtGui.QCheckBox(self.groupBox)
        self.fetchserverCheckBox.setGeometry(QtCore.QRect(10, 50, 120, 17))
        self.fetchserverCheckBox.setObjectName("fetchserverCheckBox")
        self.applyButton = QtGui.QPushButton(self.groupBox)
        self.applyButton.setGeometry(QtCore.QRect(70, 80, 75, 23))
        self.applyButton.setObjectName("applyButton")
        self.saveButton = QtGui.QPushButton(self.groupBox)
        self.saveButton.setGeometry(QtCore.QRect(240, 80, 75, 23))
        self.saveButton.setObjectName("saveButton")
        self.hideButton = QtGui.QPushButton(MainForm)
        self.hideButton.setGeometry(QtCore.QRect(170, 130, 60, 23))
        self.hideButton.setObjectName("hideButton")
        self.helpButton = QtGui.QPushButton(MainForm)
        self.helpButton.setGeometry(QtCore.QRect(170, 90, 60, 23))
        self.helpButton.setObjectName("helpButton")
        self.aboutButton = QtGui.QPushButton(MainForm)
        self.aboutButton.setGeometry(QtCore.QRect(240, 130, 60, 23))
        self.aboutButton.setObjectName("aboutButton")
        self.quitButton = QtGui.QPushButton(MainForm)
        self.quitButton.setGeometry(QtCore.QRect(310, 130, 60, 23))
        self.quitButton.setObjectName("quitButton")
        self.statusButton = QtGui.QPushButton(MainForm)
        self.statusButton.setGeometry(QtCore.QRect(30, 130, 60, 23))
        self.statusButton.setObjectName("statusButton")
        self.serviceButton = QtGui.QPushButton(MainForm)
        self.serviceButton.setGeometry(QtCore.QRect(100, 130, 60, 23))
        self.serviceButton.setObjectName("serviceButton")

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        MainForm.setWindowTitle(QtGui.QApplication.translate("MainForm", "GAppProxy", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainForm", "Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.proxyCheckBox.setText(QtGui.QApplication.translate("MainForm", "Use Local Proxy:", None, QtGui.QApplication.UnicodeUTF8))
        self.fetchserverCheckBox.setText(QtGui.QApplication.translate("MainForm", "Use FetchServer:", None, QtGui.QApplication.UnicodeUTF8))
        self.applyButton.setText(QtGui.QApplication.translate("MainForm", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("MainForm", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.hideButton.setText(QtGui.QApplication.translate("MainForm", "Hide", None, QtGui.QApplication.UnicodeUTF8))
        self.helpButton.setText(QtGui.QApplication.translate("MainForm", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutButton.setText(QtGui.QApplication.translate("MainForm", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.quitButton.setText(QtGui.QApplication.translate("MainForm", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.statusButton.setText(QtGui.QApplication.translate("MainForm", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.serviceButton.setText(QtGui.QApplication.translate("MainForm", "Service", None, QtGui.QApplication.UnicodeUTF8))

