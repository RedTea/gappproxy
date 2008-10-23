#! /usr/bin/env python
# coding=utf-8
#############################################################################
#                                                                           #
#   File: gui.pyw                                                           #
#                                                                           #
#   Copyright (C) 2008 Du XiaoGang <dugang@188.com>                         #
#                                                                           #
#   Home: http://gappproxy.googlecode.com                                   #
#                                                                           #
#   This file is part of GAppProxy.                                         #
#                                                                           #
#   GAppProxy is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU General Public License as                 #
#   published by the Free Software Foundation, either version 3 of the      #
#   License, or (at your option) any later version.                         #
#                                                                           #
#   GAppProxy is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#   GNU General Public License for more details.                            #
#                                                                           #
#   You should have received a copy of the GNU General Public License       #
#   along with GAppProxy.  If not, see <http://www.gnu.org/licenses/>.      #
#                                                                           #
#############################################################################

import sys
from PyQt4 import QtCore, QtGui
from mainform_ui import Ui_MainForm

class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./images/gap.png'))
        # create trayIcon
        self.createActions()
        self.createTrayIcon()
        # event process
        QtCore.QObject.connect(self.ui.hideButton, \
                               QtCore.SIGNAL('clicked()'), \
                               self.hideMainForm)
        QtCore.QObject.connect(self.ui.upgradeButton, \
                               QtCore.SIGNAL('clicked()'), \
                               self.checkNewVersion)
        QtCore.QObject.connect(self.ui.aboutButton, \
                               QtCore.SIGNAL('clicked()'), \
                               self.showAboutDlg)
        QtCore.QObject.connect(self.ui.quitButton, \
                               QtCore.SIGNAL('clicked()'), \
                               self.close)

    def createActions(self):
        self.restoreAction = QtGui.QAction('Restore', self)
        QtCore.QObject.connect(self.restoreAction, 
                               QtCore.SIGNAL('triggered()'), 
                               self.showMainForm)

    def createTrayIcon(self):
        # menu for trayIcon
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.restoreAction)
        # trayIcon
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QtGui.QIcon('./images/gap.png'))
        self.trayIcon.setToolTip('GAppProxy')

    def hideMainForm(self):
        self.hide()
        self.trayIcon.show()

    def showMainForm(self):
        self.showNormal()
        self.trayIcon.hide()

    def checkNewVersion(self):
        pass

    def showAboutDlg(self):
        QtGui.QMessageBox.information(self, 'About GAppProxy', 
            'GAppProxy'
            '<p>'
            'License: GPLv3'
            '<p>'
            'Version: svn r35'
            '<p>'
            'Home: <a href="http://gappproxy.googlecode.com">GAppProxy</a>'
            '<p>'
            'Maintained by: <a href="mailto:dugang@188.com">DuGang</a>'
            ' & <a href="mailto:lovelywcm@gmail.com">WCM</a>')

    def closeEvent(self, event):
        r = QtGui.QMessageBox.question(self, 'Confirm',
                                       'Do you really want to quit?', 
                                       QtGui.QMessageBox.Yes, 
                                       QtGui.QMessageBox.Cancel)
        if r != QtGui.QMessageBox.Yes:
            event.ignore()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = MainForm()
    myapp.show()
    sys.exit(app.exec_())
