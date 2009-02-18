#! /usr/bin/env python
# coding=utf-8
#############################################################################
#                                                                           #
#   File: common.py                                                         #
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

import os, sys

dir = sys.path[0]
if(hasattr(sys, 'frozen')): # py2exe
    dir = os.path.dirname(dir)

LOAD_BALANCE = 'http://gappproxy-center.appspot.com/available_fetchserver.py'
GOOGLE_PROXY = 'www.google.cn:80'
DEF_LOCAL_PROXY = ''
DEF_FETCH_SERVER = ''
DEF_LISTEN_PORT = 8000
DEF_KEY_FILE  = os.path.join(dir, 'ssl/LocalProxyServer.key')
DEF_CERT_FILE = os.path.join(dir, 'ssl/LocalProxyServer.cert')
DEF_CONF_FILE = os.path.join(dir, 'proxy.conf')
DEF_COMM_FILE = os.path.join(dir, '.proxy.conf.tmp')

class GAppProxyError(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return '<GAppProxy Error: %s>' % self.reason
