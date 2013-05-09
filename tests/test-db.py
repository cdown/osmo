#!/usr/bin/env python

import osmo.db
import time

d = osmo.db.Database(test=True)
item = {
    "name": "foo",
    "start": time.time() - 1,
    "end": time.time() + 3600,
    "length": 5,
    "priority": 1,
}

class TestDatabase(object):
    def setup(self):
        d.r.flushdb()

    def testAdd(self):
        assert all(d.add(**item))

    def testAddTwice(self):
        assert all(d.add(**item))
        assert not any(d.add(**item))

    def testRem(self):
        assert all(d.add(**item))
        assert all(d.rem(item["name"]))
