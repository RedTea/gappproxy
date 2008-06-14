#! /usr/bin/env python
# coding=utf-8
#############################################################################
#                                                                           #
#   File: proxy.py                                                          #
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

import BaseHTTPServer
import SocketServer
import urllib
import urllib2
import urlparse
import zlib

class LocalProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    PostDataLimit = 0x100000
    
    def do_METHOD(self):
        #print 'do_METHOD BEGIN!'
        # check http method and post data
        method = self.command
        if method == 'GET' or method == 'HEAD':
            # no post data
            postDataLen = 0
        elif method == 'POST':
            # get length of post data
            postDataLen = 0
            if self.headers.has_key('Content-Length'):
                postDataLen = int(self.headers['Content-Length'])
            # exceed limit?
            if postDataLen > self.PostDataLimit:
                self.send_error(403)
                self.connection.close()
                return
        else:
            # unsupported method
            self.send_error(501)
            self.connection.close()
            return

        # get post data
        postData = ''
        if postDataLen > 0:
            postData = self.rfile.read(postDataLen)
            if len(postData) != postDataLen:
                # bad request
                self.send_error(400)
                self.connection.close()
                return

        # do path check
        scm, netloc, path, params, query, frag = urlparse.urlparse(self.path)
        if scm != 'http' or not netloc:
            self.send_error(400)
            self.connection.close()
            return
        # create new path
        path = urlparse.urlunparse((scm, netloc, path, params, query, ''))

        # create request for GAppProxy
        params = urllib.urlencode({'method': method, 
                                   'path': path, 
                                   'headers': self.headers, 
                                   'encodeResponse': 'compress', 
                                   'postdata': postData})
        # accept-encoding: identity, *;q=0
        # connection: close
        #request = urllib2.Request('http://localhost:8080/fetch.py')
        request = urllib2.Request('http://dgang.appspot.com/fetch.py')
        request.add_header('Accept-Encoding', 'identity, *;q=0')
        request.add_header('Connection', 'close')
        resp = urllib2.urlopen(request, params)

        # parse resp
        textContent = True
        # for status line
        line = resp.readline()
        status = int(line.split()[1])
        self.send_response(status)
        # for headers
        while True:
            line = resp.readline()
            line = line.strip()
            # end header?
            if line == '':
                break
            # header
            name, sep, value = line.partition(':')
            name = name.strip()
            value = value.strip()
            self.send_header(name, value)
            # check Content-Type
            if name.lower() == 'content-type':
                if value.lower().find('text') == -1:
                    # not text
                    textContent = False
        self.end_headers()
        # for page
        if textContent:
            self.wfile.write(zlib.decompress(resp.read()))
        else:
            self.wfile.write(resp.read())
        self.connection.close()
        #print 'do_METHOD END!'
    
    do_GET = do_METHOD
    do_HEAD = do_METHOD
    do_POST = do_METHOD


class ThreadingHTTPServer(SocketServer.ThreadingMixIn, 
                          BaseHTTPServer.HTTPServer): 
    pass


if __name__ == '__main__':
    httpd = ThreadingHTTPServer(('127.0.0.1', 8000), LocalProxyHandler)
    httpd.serve_forever()
