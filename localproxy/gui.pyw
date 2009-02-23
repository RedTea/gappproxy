#! /usr/bin/env python
# coding=utf-8
#############################################################################
#                                                                           #
#   File: gui.pyw                                                           #
#                                                                           #
#   Copyright (C) 2008-2009 Du XiaoGang <dugang@188.com>                    #
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

import sys, os, common, win32api, win32con, win32pdhutil, win32process
from PyQt4 import QtCore, QtGui
from mainform_ui import Ui_MainForm

def readProxyAndFetchServer(confFile):
    localProxy = common.DEF_LOCAL_PROXY
    fetchServer = common.DEF_FETCH_SERVER
    # read config file
    try:
        fp = open(confFile, 'r')
    except IOError:
        # use default parameters
        return (localProxy, fetchServer)
    # parse user defined parameters
    while True:
        line = fp.readline()
        if line == '':
            # end
            break
        # parse line
        line = line.strip()
        if line == '':
            # empty line
            continue
        if line.startswith('#'):
            # comments
            continue
        (name, sep, value) = line.partition('=')
        if sep == '=':
            name = name.strip().lower()
            value = value.strip()
            if name == 'local_proxy':
                localProxy = value
            elif name == 'fetch_server':
                fetchServer = value
    return (localProxy, fetchServer)

def writeConfFile(confFile, localProxy, fetchServer):
    try:
        fp = open(confFile, 'w')
        if localProxy != common.DEF_LOCAL_PROXY:
            fp.write('local_proxy = %s\r\n' % localProxy)
        if fetchServer != common.DEF_FETCH_SERVER:
            fp.write('fetch_server = %s\r\n' % fetchServer)
        fp.close()
        return True
    except:
        return False

def isProcessAlivedByHandle(h):
    r = win32process.GetExitCodeProcess(h)
    if r == 259:    # 259 is STILL_ACTIVE
        return True
    else:
        return False

class MainForm(QtGui.QMainWindow):
    def __init__(self, proxyHandle, parent=None):
        QtGui.QWidget.__init__(self)
        self.proxyHandle = proxyHandle
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./images/gap.png'))
        # create trayIcon
        self.createActions()
        self.createTrayIcon()
        # event process
        QtCore.QObject.connect(self.ui.proxyCheckBox, \
                               QtCore.SIGNAL('clicked()'), \
                               self.useProxy)
        QtCore.QObject.connect(self.ui.fetchserverCheckBox, \
                               QtCore.SIGNAL('clicked()'), \
                               self.useFetchServer)
        QtCore.QObject.connect(self.ui.applyButton, \
                               QtCore.SIGNAL('clicked()'), \
                               self.applyChange)
        QtCore.QObject.connect(self.ui.saveButton, \
                               QtCore.SIGNAL('clicked()'), \
                               self.saveChange)
        QtCore.QObject.connect(self.ui.statusButton, \
                               QtCore.SIGNAL('clicked()'), \
                               self.checkProxyStatus)
        QtCore.QObject.connect(self.ui.hideButton, \
                               QtCore.SIGNAL('clicked()'), \
                               self.hideMainForm)
        QtCore.QObject.connect(self.ui.helpButton, \
                               QtCore.SIGNAL('clicked()'), \
                               self.showHelp)
        QtCore.QObject.connect(self.ui.aboutButton, \
                               QtCore.SIGNAL('clicked()'), \
                               self.showAboutDlg)
        QtCore.QObject.connect(self.ui.quitButton, \
                               QtCore.SIGNAL('clicked()'), \
                               self.close)
        QtCore.QObject.connect(self.ui.serviceButton, \
                               QtCore.SIGNAL('clicked()'), \
                               self.showServiceDlg)
        # read conf file
        (self.savedLocalProxy, self.savedFetchServer) = \
            readProxyAndFetchServer(common.DEF_CONF_FILE)
        self.localProxy = self.savedLocalProxy
        self.fetchServer = self.savedFetchServer
        # applyButton is disabled now
        self.ui.applyButton.setEnabled(False)
        # update control
        if self.localProxy != common.DEF_LOCAL_PROXY:
            self.ui.proxyCheckBox.setChecked(True)
            self.ui.proxyEdit.setEnabled(True)
            self.ui.proxyEdit.setText(self.localProxy)
        if self.fetchServer != common.DEF_FETCH_SERVER:
            self.ui.fetchserverCheckBox.setChecked(True)
            self.ui.fetchserverEdit.setEnabled(True)
            self.ui.fetchserverEdit.setText(self.fetchServer)

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

    def useProxy(self):
        if self.ui.proxyCheckBox.isChecked():
            self.ui.proxyEdit.setEnabled(True)
        else:
            self.ui.proxyEdit.setEnabled(False)

    def useFetchServer(self):
        if self.ui.fetchserverCheckBox.isChecked():
            self.ui.fetchserverEdit.setEnabled(True)
        else:
            self.ui.fetchserverEdit.setEnabled(False)

    def applyChange(self):
        # get new value
        if self.ui.proxyCheckBox.isChecked():
            localProxy = str(self.ui.proxyEdit.text())
        else:
            localProxy = common.DEF_LOCAL_PROXY
        if self.ui.fetchserverCheckBox.isChecked():
            fetchServer = str(self.ui.fetchserverEdit.text())
        else:
            fetchServer = common.DEF_FETCH_SERVER
        localProxy = localProxy.strip()
        fetchServer = fetchServer.strip()
        # should write?
        if localProxy != self.localProxy or fetchServer != self.fetchServer:
            self.localProxy = localProxy
            self.fetchServer = fetchServer
            writeConfFile(common.DEF_COMM_FILE, localProxy, fetchServer)

    def saveChange(self):
        # get new value
        if self.ui.proxyCheckBox.isChecked():
            localProxy = str(self.ui.proxyEdit.text())
        else:
            localProxy = common.DEF_LOCAL_PROXY
        if self.ui.fetchserverCheckBox.isChecked():
            fetchServer = str(self.ui.fetchserverEdit.text())
        else:
            fetchServer = common.DEF_FETCH_SERVER
        localProxy = localProxy.strip()
        fetchServer = fetchServer.strip()
        # always write
        if not writeConfFile(common.DEF_CONF_FILE, localProxy, fetchServer):
            QtGui.QMessageBox.warning(self, 'Error', 'Write Error!')
        else:
            QtGui.QMessageBox.information(self, 'OK', 'Done!')
        ## should write?
        #if localProxy != self.savedLocalProxy \
        #   or fetchServer != self.savedFetchServer:
        #    self.savedLocalProxy = localProxy
        #    self.savedFetchServer = fetchServer
        #    writeConfFile(common.DEF_CONF_FILE, localProxy, fetchServer)

    def checkProxyStatus(self):
        if isProcessAlivedByHandle(self.proxyHandle):
            QtGui.QMessageBox.information(self, 'OK', 'Proxy is running!')
        else:
            QtGui.QMessageBox.warning(self, 'Error', 
                                      'Proxy is exit, restart GAppProxy please!')

    def hideMainForm(self):
        self.hide()
        self.trayIcon.show()

    def showMainForm(self):
        self.showNormal()
        self.trayIcon.hide()

    def showHelp(self):
        QtGui.QMessageBox.information(self, 'Help', 
            '<table border="0" align="center">\r\n'
            '<tr><th align="center" colspan="2">Help</th></tr>\r\n'
            '<tr><td align="center" colspan="2"><hr></td></tr>\r\n'
            '<tr><td>Save: </td><td>Save user defined parameters to the default configuration file.</td></tr>\r\n'
            '<tr><td>Status: </td><td>Check whether the proxy kernel is running or not.</td></tr>\r\n'
            '<tr><td>Hide: </td><td>Hide this window and show a icon in the system tray.</td></tr>\r\n'
            '<tr><td align="center" colspan="2"><hr></td></tr>\r\n'
            '<tr><td align="center" colspan="2">For more information, see <a href="http://gappproxy.googlecode.com">GAppProxy\'s Home</a>.</td></tr>\r\n'
            '</table>\r\n')

    def showAboutDlg(self):
        QtGui.QMessageBox.information(self, 'About GAppProxy', 
            '<table border="0" align="center">\r\n'
            '<tr><th align="center" colspan="2">GAppProxy</th></tr>\r\n'
            '<tr><td align="center" colspan="2"></td></tr>\r\n'
            '<tr><td align="center" colspan="2">A free HTTP proxy based on Google App Engine.</td></tr>\r\n'
            '<tr><td align="center" colspan="2"><hr></td></tr>\r\n'
            '<tr><td align="center" colspan="2">Version: 1.0.0 beta</td></tr>\r\n'
            '<tr><td align="center" colspan="2">License: GPLv3</td></tr>\r\n'
            '<tr><td align="center" colspan="2">Home: <a href="http://gappproxy.googlecode.com">GAppProxy</a></td></tr>\r\n'
            '<tr><td align="center" colspan="2"><hr></td></tr>\r\n'
            '<tr><td align="right">Maintained by:</td><td align="left"><a href="mailto:dugang@188.com">DuGang</a></td></tr>\r\n'
            '<tr><td></td><td align="left"><a href="mailto:lovelywcm@gmail.com">WCM</a></td></tr>\r\n'
            '</table>\r\n')

    def closeEvent(self, event):
        r = QtGui.QMessageBox.question(self, 'Confirm',
                                       'Do you really want to quit?', 
                                       QtGui.QMessageBox.Yes, 
                                       QtGui.QMessageBox.Cancel)
        if r != QtGui.QMessageBox.Yes:
            event.ignore()

    def showServiceDlg(self):
        # yeah, twice, or will get incorrect exit status. Don't know why, maybe a bug?
        if os.spawnl(os.P_WAIT, 'service\query.bat', 'service\query.bat') == 0:
            s = QtGui.QMessageBox.question(self, 'Remove service?',
                'You have registered GAppProxy as a system service.\r\n\r\n'
                'Do you want to remove it?\r\n\r\n'
                'Note: Vista users need to\r\n'
                'right click "gui.exe" and choose "Run as Administrator" first.',
                                        QtGui.QMessageBox.Yes,
                                        QtGui.QMessageBox.Cancel)
            if s == QtGui.QMessageBox.Yes:
                if os.spawnl(os.P_WAIT, 'service\uninstall.bat', 'service\uninstall.bat') != 0:
                    QtGui.QMessageBox.warning(self, 'failed', 'Please run as administrator')
                else:
                    QtGui.QMessageBox.information(self, 'Successful',
                        'As you wish, GAppProxy service has been removed.')
        else:
            s = QtGui.QMessageBox.question(self, 'Register GAppProxy as a system service?',
                'Do you want to register GAppProxy as a system service?\r\n\r\n'
                'Thus you don\'t need to run it manually every time.\r\n\r\n'
                'Note: Vista users need to\r\n'
                'right click "gui.exe" and choose "Run as Administrator" first.',
                                        QtGui.QMessageBox.Yes, 
                                        QtGui.QMessageBox.Cancel)
            if s == QtGui.QMessageBox.Yes:
                if os.spawnl(os.P_WAIT, 'service\install.bat', 'service\install.bat') != 0:
                    QtGui.QMessageBox.warning(self, 'failed', 'Please run as administrator')
                else:
                    QtGui.QMessageBox.information(self, 'Successful',
                        'Great!\r\nGAppProxy is ready to serve, you can quit this program now.')

def kill_WIN32(pid):
    h = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, pid)
    win32api.TerminateProcess(h, 0)
    win32api.CloseHandle(h)

def killByHandle(h):
    win32api.TerminateProcess(h, 0)
    win32api.CloseHandle(h)

def killall_WIN32(name):
    pids = win32pdhutil.FindPerformanceAttributesByName(name)
    for pid in pids:
        kill_WIN32(pid)

if __name__ == '__main__':
    # clear run env
    try:
        os.remove(common.DEF_COMM_FILE)
        killall_WIN32('proxy')
    except:
        pass
    # run proxy server
    h = os.spawnl(os.P_NOWAIT, './proxy.exe', './proxy.exe')
    # GUI
    app = QtGui.QApplication(sys.argv)
    myapp = MainForm(h)
    myapp.show()
    r = app.exec_()
    try:
        killByHandle(h)
    except:
        pass
    sys.exit(r)
