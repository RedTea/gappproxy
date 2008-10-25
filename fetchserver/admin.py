#! /usr/bin/env python
# coding=utf-8
#############################################################################
#                                                                           #
#   File: admin.py                                                          #
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

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.api import users
import accesslog

class MainHandler(webapp.RequestHandler):
    def listPopDesti(self, count):
        # format
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write( \
'''<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
        <title>GAppProxy 热门站点统计</title>
    </head>
    <body>
        <table width="800" border="1" align="center">
            <tr><th colspan="2">GAppProxy 热门站点统计（TOP %d）</th></tr>
            <tr><th>站点</th><th>访问量</th></tr>
''' % count)
        ds = accesslog.listPopDesti(count)
        for d in ds:
            self.response.out.write( \
'''            <tr><td>%s</td><td>%d</td></tr>
''' % (str(d[0]), d[1]))
        self.response.out.write( \
'''        </table>
    </body>
</html>
''')

    def listFreqFro(self, count):
        # format
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write( \
'''<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
        <title>GAppProxy 用户使用统计</title>
    </head>
    <body>
        <table width="800" border="1" align="center">
            <tr><th colspan="2">GAppProxy 用户使用统计（TOP %d）</th></tr>
            <tr><th>用户 IP</th><th>访问量</th></tr>
''' % count)
        ds = accesslog.listFreqFro(count)
        for d in ds:
            self.response.out.write( \
'''            <tr><td>%s</td><td>%d</td></tr>
''' % (str(d[0]), d[1]))
        self.response.out.write( \
'''        </table>
    </body>
</html>
''')

    def get(self):
        user = users.get_current_user()
        obj = self.request.get('obj')
        cmd = self.request.get('cmd')
        # check
        if user:
            if user.email() == 'dugang@188.com':
                # OK, dispatch
                if obj.lower() == 'accesslog':
                    # for AccessLog
                    if cmd.lower() == 'clear':
                        # clear log
                        accesslog.clearAll()
                        self.response.headers['Content-Type'] = 'text/plain'
                        self.response.out.write('Clear OK!')
                    elif cmd.lower() == 'list_pop_desti':
                        # list the most popular destinations
                        self.listPopDesti(50)
                    elif cmd.lower() == 'list_freq_fro':
                        # list the most frequent user
                        self.listFreqFro(50)
                    else:
                        self.response.headers['Content-Type'] = 'text/plain'
                        self.response.out.write('Wrong cmd!')
                else:
                    self.response.headers['Content-Type'] = 'text/plain'
                    self.response.out.write('Wrong obj!')
            else:
                # FAILED, send response
                self.response.headers['Content-Type'] = 'text/plain'
                self.response.out.write('Forbidden!')
        else:
            # 'clear accesslog' is an exception, for batch operation
            if obj.lower() == 'accesslog' and cmd.lower() == 'clear':
                # need magic number
                magic = self.request.get('magic')
                if False:
                #if magic == '':
                    # clear log
                    accesslog.clearAll()
                    self.response.headers['Content-Type'] = 'text/plain'
                    self.response.out.write('Clear OK!')
                else:
                    self.response.headers['Content-Type'] = 'text/plain'
                    self.response.out.write('Forbidden!')
            else:
                self.redirect(users.create_login_url(self.request.uri))

def main():
    application = webapp.WSGIApplication([('/admin.py', MainHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
