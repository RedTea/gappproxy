#! /usr/bin/env python
# coding=utf-8
#############################################################################
#                                                                           #
#   File: available_fetchserver.py                                          #
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
