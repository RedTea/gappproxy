#! /usr/bin/env python
# coding=utf-8
#############################################################################
#                                                                           #
#   File: available_fetchserver.py                                          #
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
import random

class MainHandler(webapp.RequestHandler):
    def get(self):
        fss = ['http://fetchserver1.appspot.com/fetch.py', 
               'http://fetchserver2.appspot.com/fetch.py', 
               'http://fetchserver3.appspot.com/fetch.py', 
               'http://wcm.appspot.com/fetch.py', 
               'http://fetchserver-nolog.appspot.com/fetch.py']
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(fss[random.randint(0, len(fss) - 1)])

def main():
    application = webapp.WSGIApplication([('/available_fetchserver.py', MainHandler)])
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
