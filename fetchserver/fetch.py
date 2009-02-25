#! /usr/bin/env python
# coding=utf-8
#############################################################################
#                                                                           #
#   File: fetch.py                                                          #
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

import wsgiref.handlers, urlparse, StringIO, logging, base64, zlib
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors
# from accesslog import logAccess


class MainHandler(webapp.RequestHandler):
    Software = 'GAppProxy/1.0.0 beta'
    # hop to hop header should not be forwarded
    HtohHdrs= ['connection', 'keep-alive', 'proxy-authenticate',
               'proxy-authorization', 'te', 'trailers',
               'transfer-encoding', 'upgrade']

    def myError(self, status, description, encodeResponse):
        # header
        self.response.out.write('HTTP/1.1 %d %s\r\n' % (status, description))
        self.response.out.write('Server: %s\r\n' % self.Software)
        self.response.out.write('Content-Type: text/html\r\n')
        self.response.out.write('\r\n')
        # body
        content = '<h1>Fetch Server Error</h1><p>Error Code: %d<p>Message: %s' % (status, description)
        if encodeResponse == 'base64':
            self.response.out.write(base64.b64encode(content))
        elif encodeResponse == 'compress':
            self.response.out.write(zlib.compress(content))
        else:
            self.response.out.write(content)

    def post(self):
        try:
            # get post data
            origMethod = self.request.get('method')
            origPath = self.request.get('encoded_path')
            if origPath != '':
                origPath = base64.b64decode(origPath)
            else:
                origPath = self.request.get('path')
            origHeaders = self.request.get('headers')
            encodeResponse = self.request.get('encodeResponse')
            origPostData = self.request.get('postdata')

            # check method
            if origMethod != 'GET' and origMethod != 'HEAD' \
               and origMethod != 'POST':
                # forbid
                self.myError(590, 'Invalid local proxy, Method not allowed.', encodeResponse)
                return
            if origMethod == 'GET':
                method = urlfetch.GET
            elif origMethod == 'HEAD':
                method = urlfetch.HEAD
            elif origMethod == 'POST':
                method = urlfetch.POST

            # check path
            (scm, netloc, path, params, query, _) = urlparse.urlparse(origPath)
            if (scm.lower() != 'http' and scm.lower() != 'https') or not netloc:
                self.myError(590, 'Invalid local proxy, Unsupported Scheme.', encodeResponse)
                return
            # create new path
            newPath = urlparse.urlunparse((scm, netloc, path, params, query, ''))

            # make new headers
            newHeaders = {}
            contentLength = 0
            si = StringIO.StringIO(origHeaders)
            while True:
                line = si.readline()
                line = line.strip()
                if line == '':
                    break
                # parse line
                (name, _, value) = line.partition(':')
                name = name.strip()
                value = value.strip()
                if name.lower() in self.HtohHdrs:
                    # don't forward
                    continue
                newHeaders[name] = value
                if name.lower() == 'content-length':
                    contentLength = int(value)
            # predined header
            newHeaders['Connection'] = 'close'

            # check post data
            if contentLength != 0:
                if contentLength != len(origPostData):
                    self.myError(590, 'Invalid local proxy, Wrong length of post data.',
                                 encodeResponse)
                    return
            else:
                origPostData = ''

            if origPostData != '' and origMethod != 'POST':
                self.myError(590, 'Invalid local proxy, Inconsistent method and data.',
                             encodeResponse)
                return
        except Exception, e:
            self.myError(591, 'Fetch server error, %s.' % str(e), encodeResponse)
            return

        # fetch, try 3 times
        for _ in range(3):
            try:
                resp = urlfetch.fetch(newPath, origPostData, method, newHeaders, False, False)
                break
            except urlfetch_errors.ResponseTooLargeError:
                self.myError(591, 'Fetch server error, Sorry, Google\'s limit, file size up to 1MB.', encodeResponse)
                return
            except Exception:
                continue
        else:
            self.myError(591, 'Fetch server error, The target server may be down or not exist. Another possibility: try to request the URL directly.', encodeResponse)
            return

        # forward
        self.response.headers['Content-Type'] = 'application/octet-stream'
        # status line
        self.response.out.write('HTTP/1.1 %d %s\r\n' % (resp.status_code, \
                                self.response.http_status_message(resp.status_code)))
        # headers
        # default Content-Type is text
        textContent = True
        for header in resp.headers:
            if header.strip().lower() in self.HtohHdrs:
                # don't forward
                continue
            ## there may have some problems on multi-cookie process in urlfetch.
            #if header.lower() == 'set-cookie':
            #    logging.info('O %s: %s' % (header, resp.headers[header]))
            #    scs = resp.headers[header].split(',')
            #    for sc in scs:
            #        logging.info('N %s: %s' % (header, sc.strip()))
            #        self.response.out.write('%s: %s\r\n' % (header, sc.strip()))
            #    continue
            # other
            self.response.out.write('%s: %s\r\n' % (header, resp.headers[header]))
            # check Content-Type
            if header.lower() == 'content-type':
                if resp.headers[header].lower().find('text') == -1:
                    # not text
                    textContent = False
        self.response.out.write('\r\n')
        # need encode?
        if encodeResponse == 'base64':
            self.response.out.write(base64.b64encode(resp.content))
        elif encodeResponse == 'compress':
            # only compress when Content-Type is text/xxx
            if textContent:
                self.response.out.write(zlib.compress(resp.content))
            else:
                self.response.out.write(resp.content)
        else:
            self.response.out.write(resp.content)

        # log
        #logAccess(netloc, self.request.remote_addr)

    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.out.write( \
'''
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>GAppProxy已经在工作了</title>
    </head>
    <body>
        <table width="800" border="0" align="center">
            <tr><td align="center"><hr></td></tr>
            <tr><td align="center">
                <b><h1>%s 已经在工作了</h1></b>
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
''' % self.Software)


def main():
    application = webapp.WSGIApplication([('/fetch.py', MainHandler)])
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
