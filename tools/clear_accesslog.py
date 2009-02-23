#! /usr/bin/env python
# coding=utf-8
#############################################################################
#                                                                           #
#   File: clear_accesslog.py                                                #
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

import urllib2, sys

def clear():
    while True:
        try:
            request = urllib2.Request('http://fetchserver3.appspot.com/admin.py?obj=accesslog&cmd=clear&magic=')
            proxy_handler = urllib2.ProxyHandler({'http': 'www.google.cn:80'})
            opener = urllib2.build_opener(proxy_handler)
            # set the opener as the default opener
            urllib2.install_opener(opener)
            resp = urllib2.urlopen(request)
            print resp.read()
            break
        except Exception:
            print '.'
            sys.stdout.flush()
            continue

if __name__ == '__main__':
    clear()
