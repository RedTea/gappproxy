#! /usr/bin/env python
# coding=utf-8
#############################################################################
#                                                                           #
#   File: fetch.py                                                          #
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
import urlparse
import StringIO
import logging
import base64
import zlib
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import urlfetch


class FetchFromIP(db.Model):
    fromIP = db.StringProperty(required=True)
    successedCount = db.IntegerProperty()
    failedCount = db.IntegerProperty()


class MainHandler(webapp.RequestHandler):
    Software = 'GAppProxy/0.0.1'
    # hop to hop header should not be forwarded
    HtohHdrs= ['connection', 'keep-alive', 'proxy-authenticate',
               'proxy-authorization', 'te', 'trailers',
               'transfer-encoding', 'upgrade']

    def myerror(self, status):
        self.response.out.write('HTTP/1.1 %d %s\r\n' % (status, \
                                self.response.http_status_message(status)))
        self.response.out.write('Server: %s\r\n' % self.Software)
        self.response.out.write('\r\n')

    def log(self, srcIP, url, successed=True):
        # for FetchFromIP
        # search
        res = db.GqlQuery('SELECT * FROM FetchFromIP WHERE fromIP=:1', srcIP)
        nr = 0
        for re in res:
            nr += 1
        if nr == 0:
            # need create
            if successed:
                re = FetchFromIP(fromIP=srcIP, successedCount=1, failedCount=0)
            else:
                re = FetchFromIP(fromIP=srcIP, successedCount=0, failedCount=1)
            re.put()
        elif nr == 1:
            # need update
            if successed:
                re.successedCount += 1
            else:
                re.failedCount += 1
            re.put()
        else:
            # error
            logging.error('What?FromIP!')

    def post(self):
        try:
            # get post data
            origMethod = self.request.get('method')
            origPath = self.request.get('path')
            origHeaders = self.request.get('headers')
            encodeResponse = self.request.get('encodeResponse')
            origPostData = self.request.get('postdata')

            # check method
            if origMethod != 'GET' and origMethod != 'HEAD' \
               and origMethod != 'POST':
                # forbid
                self.myerror(403)
                self.log(self.request.remote_addr, origPath, False)
                return
            if origMethod == 'GET':
                method = urlfetch.GET
            elif origMethod == 'HEAD':
                method = urlfetch.HEAD
            elif origMethod == 'POST':
                method = urlfetch.POST

            # check path
            scm, netloc, path, params, query, frag = urlparse.urlparse(origPath)
            if scm != 'http' or not netloc:
                self.myerror(403)
                self.log(self.request.remote_addr, origPath, False)
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
                name, sep, value = line.partition(':')
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
                    self.myerror(403)
                    self.log(self.request.remote_addr, origPath, False)
                    return
            else:
                origPostData = ''

            if origPostData != '' and origMethod != 'POST':
                self.myerror(403)
                self.log(self.request.remote_addr, origPath, False)
                return
        except Exception:
            self.myerror(403)
            self.log(self.request.remote_addr, origPath, False)
            return

        # fetch
        try:
            resp = urlfetch.fetch(newPath, origPostData, method, newHeaders)
        except Exception, e:
            self.myerror(500)
            self.log(self.request.remote_addr, origPath, False)
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
            # maybe there are some problems on multi-cookie process in urlfetch.
            if header.lower() == 'set-cookie':
                scs = resp.headers[header].split(',')
                for sc in scs:
                    #logging.info('%s: %s' % (header, sc.strip()))
                    self.response.out.write('%s: %s\r\n' % (header, sc.strip()))
                continue
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
        # log it
        self.log(self.request.remote_addr, newPath, True)


def main():
    application = webapp.WSGIApplication([('/fetch.py', MainHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
