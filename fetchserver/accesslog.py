#! /usr/bin/env python
# coding=utf-8
#############################################################################
#                                                                           #
#   File: accesslog.py                                                      #
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

from google.appengine.ext import db

class AccessDestination(db.Model):
    desti = db.StringProperty(required=True)
    counter = db.IntegerProperty(required=True)

class AccessFrom(db.Model):
    fro = db.StringProperty(required=True)
    counter = db.IntegerProperty(required=True)

def incDestiCounter(desti):
    rec = db.get(db.Key.from_path('AccessDestination', 'D:%s' % desti))
    if not rec:
        rec = AccessDestination(desti=desti, counter=1, key_name='D:%s' % desti)
    else:
        rec.counter += 1
    rec.put()

def incFroCounter(fro):
    rec = db.get(db.Key.from_path('AccessFrom', 'F:%s' % fro))
    if not rec:
        rec = AccessFrom(fro=fro, counter=1, key_name='F:%s' % fro)
    else:
        rec.counter += 1
    rec.put()

def logAccess(desti, fro):
    try:
        db.run_in_transaction(incDestiCounter, desti)
        db.run_in_transaction(incFroCounter, fro)
        return True
    except Exception:
        return False

def listPopDesti(count):
    ls = []
    q = db.GqlQuery("select * from AccessDestination order by counter desc")
    results = q.fetch(count)
    for r in results:
        ls.append((r.desti, r.counter))
    return ls

def listFreqFro(count):
    ls = []
    q = db.GqlQuery("select * from AccessFrom order by counter desc")
    results = q.fetch(count)
    for r in results:
        ls.append((r.fro, r.counter))
    return ls

def clearDesti():
    recs = AccessDestination.all()
    for r in recs:
        r.delete()

def clearFro():
    recs = AccessFrom.all()
    for r in recs:
        r.delete()

def clearAll():
    clearDesti()
    clearFro()
