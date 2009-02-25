#! /usr/bin/env python
# coding=utf-8
#############################################################################
#                                                                           #
#   File: proxy.py                                                          #
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

import BaseHTTPServer, SocketServer, urllib, urllib2, urlparse, zlib, \
       socket, os, common, sys, errno, base64
try:
    import ssl
    SSLEnable = True
except:
    SSLEnable = False

# global varibles
localProxy = common.DEF_LOCAL_PROXY
fetchServer = common.DEF_FETCH_SERVER
google_proxy_or_not = {}

class LocalProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    PostDataLimit = 0x100000

    def do_CONNECT(self):
        if not SSLEnable:
            self.send_error(501, 'Local proxy error, HTTPS needs Python2.6 or later.')
            self.connection.close()
            return

        # for ssl proxy
        (httpsHost, _, httpsPort) = self.path.partition(':')
        if httpsPort != '' and httpsPort != '443':
            self.send_error(501, 'Local proxy error, Only port 443 is allowed for https.')
            self.connection.close()
            return

        # continue
        self.wfile.write('HTTP/1.1 200 OK\r\n')
        self.wfile.write('\r\n')
        sslSock = ssl.SSLSocket(self.connection, 
                                server_side=True, 
                                certfile=common.DEF_CERT_FILE,
                                keyfile=common.DEF_KEY_FILE)

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
        (method, path, ver) = firstLine.split()
        if path.startswith('/'):
            path = 'https://%s' % httpsHost + path

        # connect to local proxy server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', common.DEF_LISTEN_PORT))
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
                    sock.close()
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
        sslSock.close()
        self.connection.close()
    
    def do_METHOD(self):
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
                self.send_error(413, 'Local proxy error, Sorry, Google\'s limit, file size up to 1MB.')
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
        (scm, netloc, path, params, query, _) = urlparse.urlparse(self.path)
        if (scm.lower() != 'http' and scm.lower() != 'https') or not netloc:
            self.send_error(501, 'Local proxy error, Unsupported scheme(ftp for example).')
            self.connection.close()
            return
        # create new path
        path = urlparse.urlunparse((scm, netloc, path, params, query, ''))

        # create request for GAppProxy
        params = urllib.urlencode({'method': method, 
                                   #'path': path, 
                                   'encoded_path': base64.b64encode(path), 
                                   'headers': self.headers, 
                                   'encodeResponse': 'compress', 
                                   'postdata': postData, 
                                   'version': '1.0.0 beta'})
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
            proxy_handler = urllib2.ProxyHandler(google_proxy_or_not)
        opener = urllib2.build_opener(proxy_handler)
        # set the opener as the default opener
        urllib2.install_opener(opener)
        try:
            resp = urllib2.urlopen(request, params)
        except urllib2.HTTPError, errMsg:
            errNum = int( str(errMsg).split(' ')[2].split(':')[0] )
            if errNum == 404:
                self.send_error(404, 'Local proxy error, Fetchserver not found at the URL you specified, please check it.')
            elif errNum == 502:
                self.send_error(502, 'Local proxy error, Invalid response from fetchserver, an occasional transmission error, or the fetchserver is too busy.')
            else:
                self.send_error(errNum)
            self.connection.close()
            return

        # parse resp
        textContent = True
        # for status line
        line = resp.readline()
        words = line.split()
        status = int(words[1])
        reason = ' '.join(words[2:])
        try:
            self.send_response(status, reason)
        except socket.error, (errNum, _): 
            # Connection/Webpage closed before proxy return
            if errNum == errno.EPIPE or errNum == 10053: # *nix, Windows
                return
            else:
                raise

        # for headers
        while True:
            line = resp.readline()
            line = line.strip()
            # end header?
            if line == '':
                break
            # header
            (name, _, value) = line.partition(':')
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

    do_GET = do_METHOD
    do_HEAD = do_METHOD
    do_POST = do_METHOD

class ThreadingHTTPServer(SocketServer.ThreadingMixIn, 
                          BaseHTTPServer.HTTPServer): 
    pass

def shallWeNeedDefaultProxy():
    global google_proxy_or_not

    # send http request directly
    request = urllib2.Request(common.LOAD_BALANCE)
    try:
        # avoid wait too long at startup, timeout argument need py2.6 or later.
        if sys.hexversion > 0x20600f0:
            resp = urllib2.urlopen(request, timeout=30)
        else:
            resp = urllib2.urlopen(request)
        resp.read()
    except:
        google_proxy_or_not = {'http': common.GOOGLE_PROXY}

def getAvailableFetchServer():
    request = urllib2.Request(common.LOAD_BALANCE)
    if localProxy != '':
        proxy_handler = urllib2.ProxyHandler({'http': localProxy})
    else:
        proxy_handler = urllib2.ProxyHandler(google_proxy_or_not)
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)
    try:
        resp = urllib2.urlopen(request)
        return resp.read().strip()
    except:
        return ''

def parseConf(confFile):
    global localProxy, fetchServer

    # read config file
    try:
        fp = open(confFile, 'r')
    except IOError:
        # use default parameters
        return
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
    fp.close()

if __name__ == '__main__':
    print '--------------------------------------------'
    if SSLEnable:
        print 'HTTP Enabled : YES'
        print 'HTTPS Enabled: YES'
    else:
        print 'HTTP Enabled : YES'
        print 'HTTPS Enabled: NO'

    parseConf(common.DEF_CONF_FILE)

    if localProxy == '':
        shallWeNeedDefaultProxy()

    if fetchServer == '':
        fetchServer = getAvailableFetchServer()
    if fetchServer == '':
        raise common.GAppProxyError('Invalid response from load balance server.')

    # Want to know whether you are connect to fetchserver direct? uncomment it.
    print 'Direct Fetch : %s' % ( google_proxy_or_not and 'NO' or 'YES' )
    print 'Local Proxy  : %s' % localProxy
    print 'Fetch Server : %s' % fetchServer
    print '--------------------------------------------'
    httpd = ThreadingHTTPServer(('', common.DEF_LISTEN_PORT), 
                                LocalProxyHandler)
    httpd.serve_forever()

    # for 'Apply' in GUI
    #while True:
    #    # parameters changed?
    #    if os.path.exists(common.DEF_COMM_FILE):
    #        # renew
    #        localProxy = common.DEF_LOCAL_PROXY
    #        fetchServer = common.DEF_FETCH_SERVER
    #        parseConf(common.DEF_COMM_FILE)
    #        os.remove(common.DEF_COMM_FILE)
    #        if fetchServer == '':
    #            fetchServer = getAvailableFetchServer()
    #        if fetchServer == '':
    #            raise common.GAppProxyError('Invalid response from load balance server.')
    #        print 'Local Proxy  : %s' % localProxy
    #        print 'Fetch Server : %s' % fetchServer
    #    # do handle
    #    httpd.handle_request()
