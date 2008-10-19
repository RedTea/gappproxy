#! /usr/bin/env python

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
        except BaseException:
            print '.'
            sys.stdout.flush()
            continue

if __name__ == '__main__':
    clear()
