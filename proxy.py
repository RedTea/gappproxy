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
import socket
try:
    import ssl
    SSLEnable = True
except:
    SSLEnable = False
import random

class LocalProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    global localProxy, fetchServer

    PostDataLimit = 0x100000

    def do_CONNECT(self):
        if not SSLEnable:
            # Not Implemented
            print 'HTTPS is not enabled: HTTPS needs Python 2.6 or later.'
            self.wfile.write('HTTP/1.1 501 Not Implemented\r\n')
            self.wfile.write('\r\n')
            self.connection.close()
            return
            
        # for ssl proxy
        httpsHost, sep, httpsPort = self.path.partition(':')
        if httpsPort != '' and httpsPort != '443':
            # unsupport
            self.wfile.write('HTTP/1.1 403 Forbidden\r\n')
            self.wfile.write('\r\n')
            self.connection.close()
            return

        # continue
        self.wfile.write('HTTP/1.1 200 OK\r\n')
        self.wfile.write('\r\n')
        sslSock = ssl.SSLSocket(self.connection, 
                                server_side=True, 
                                certfile='./LocalProxyServer.cert', 
                                keyfile='./LocalProxyServer.key')

        # rewrite request line, url to abs
        firstLine = ''
        while True:
            chr = sslSock.read(1)
            # EOF?
            if chr == '':
                # bad request
                sslSock.close()
                self.connection.close()
                return
            # newline(\r\n)?
            if chr == '\r':
                chr = sslSock.read(1)
                if chr == '\n':
                    # got
                    break
                else:
                    # bad request
                    sslSock.close()
                    self.connection.close()
                    return
            # newline(\n)?
            if chr == '\n':
                # got
                break
            firstLine += chr

        # get path
        method, path, ver = firstLine.split()
        if path.startswith('/'):
            path = 'https://%s' % httpsHost + path

        # connect to local proxy server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 8000))
        sock.send('%s %s %s\r\n' % (method, path, ver))

        # forward https request
        sslSock.settimeout(1)
        while True:
            try:
                data = sslSock.read(8192)
            except ssl.SSLError, e:
                if str(e).lower().find('timed out') == -1:
                    # error
                    sslSock.close()
                    self.connection.close()
                    return
                # timeout
                break
            if data != '':
                sock.send(data)
            else:
                # EOF
                break
        sslSock.setblocking(True)

        # simply forward response
        while True:
            data = sock.recv(8192)
            if data != '':
                sslSock.write(data)
            else:
                # EOF
                break

        # clean
        sock.close()
        sslSock.shutdown(socket.SHUT_WR)
        self.connection.close()
    
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
        if (scm.lower() != 'http' and scm.lower() != 'https') or not netloc:
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
        request = urllib2.Request(fetchServer)
        request.add_header('Accept-Encoding', 'identity, *;q=0')
        request.add_header('Connection', 'close')
        # create new opener
        if localProxy != '':
            proxy_handler = urllib2.ProxyHandler({'http': localProxy})
        else:
            proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(proxy_handler)
        # set the opener as the default opener
        urllib2.install_opener(opener)
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
            dat = resp.read()
            if len(dat) > 0:
                self.wfile.write(zlib.decompress(dat))
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


def parseConf(confFile):
    global localProxy, fetchServer

    fetchServers = []

    # read config file
    fp = open(confFile, 'r')
    while True:
        line = fp.readline()
        if line == '':
            # end
            break
        # parse line
        line = line.strip()
        if line.startswith('#'):
            # comments
            continue
        (name, sep, value) = line.partition('=')
        name = name.strip().lower()
        value = value.strip()
        if name == 'local_proxy':
            localProxy = value
        elif name == 'fetch_server':
            fetchServers.append(value)

    # check
    if len(fetchServers) == 0:
        # no fetch server
        print 'I cat\'t get any fetch_server from proxy.conf.'
        return False

    # random select
    if len(fetchServers) > 1:
        fetchServer = fetchServers[random.randint(0, len(fetchServers) - 1)]
    else:
        fetchServer = fetchServers[0]
    return True


if __name__ == '__main__':
    global localProxy, fetchServer

    if SSLEnable:
        print '--------------------------------------------'
        print 'HTTP Enabled : YES'
        print 'HTTPS Enabled: YES'
    else:
        print 'HTTP Enabled : YES'
        print 'HTTPS Enabled: NO'

    localProxy = ''
    fetchServer = ''
    if parseConf('./proxy.conf'):
        print 'Local Proxy: %s' % localProxy
        print 'Fetch Server: %s' % fetchServer
        print '--------------------------------------------'
        httpd = ThreadingHTTPServer(('', 8000), LocalProxyHandler)
        httpd.serve_forever()
