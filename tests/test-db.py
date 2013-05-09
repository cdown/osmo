#!/usr/bin/env python

import osmo.db
import time

d = osmo.db.Database(test=True)
now = time.time()
items = {
    "current":{
        "name": "foo",
        "start": now - 1,
        "end": now + 3600,
        "length": 5,
        "priority": 1,
    },
    "past":{
        "name": "foo",
        "start": now - 2,
        "end": now - 1,
        "length": 5,
        "priority": 1,
    },
    "future":{
        "name": "foo",
        "start": now + 3600,
        "end": now + 7200,
        "length": 5,
        "priority": 1,
    },
}

class TestDatabase(object):
    def setup(self):
        d.r.flushdb()

    def testAdd(self):
        assert all(d.add(**items["current"]))

    def testAddTwice(self):
        assert all(d.add(**items["current"]))
        assert not any(d.add(**items["current"]))

    def testRem(self):
        assert all(d.add(**items["current"]))
        assert all(d.rem(items["current"]["name"]))

    def testRemVoid(self):
        assert not any(d.rem(items["current"]["name"]))
