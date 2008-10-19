#! /usr/bin/env python
# coding=utf-8
#############################################################################
#                                                                           #
#   File: main.py                                                           #
#                                                                           #
#   Copyright (C) 2008 Du XiaoGang <dugang@188.com>                         #
#                                                                           #
#   This program is free software; you can redistribute it and/or modify    #
#   it under the terms of the GNU General Public License as published by    #
#   the Free Software Foundation; either version 2 of the License, or       #
#   (at your option) any later version.                                     #
#                                                                           #
#   Home: http://gappproxy.googlecode.com                                   #
#   Blog: http://inside2004.cublog.cn                                       #
#                                                                           #
#############################################################################

import wsgiref.handlers
from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.out.write( \
'''
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>GAppProxy Center</title>
    </head>
    <body>
        <table width="800" border="0" align="center">
            <tr><td align="center"><hr></td></tr>
            <tr><td align="center">
                <b><h1>GAppProxy Center</h1></b>
            </td></tr>
            <tr><td align="center"><hr></td></tr>

            <tr><td align="center">
                GAppProxy是一个开源的HTTP Proxy软件,使用Python编写,运行于Google App Engine平台上. 
            </td></tr>
            <tr><td align="center"><hr></td></tr>

            <tr><td align="center">
                更多相关介绍,请参考<a href="http://gappproxy.googlecode.com/">GAppProxy项目主页</a>. 
            </td></tr>
            <tr><td align="center"><hr></td></tr>

            <tr><td align="center">
                <img src="http://code.google.com/appengine/images/appengine-silver-120x30.gif" alt="Powered by Google App Engine" />
            </td></tr>
            <tr><td align="center"><hr></td></tr>
        </table>
    </body>
</html>
''')

def main():
    application = webapp.WSGIApplication([('.*', MainHandler)])
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
