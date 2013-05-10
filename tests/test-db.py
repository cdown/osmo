#!/usr/bin/env python

import osmo.db
import time

d = osmo.db.Database(test=True)
now = time.time()
items = {
    "current":{
        "name": "current",
        "start": now - 1,
        "end": now + 3600,
        "span": 5,
        "rank": 1,
    },
    "past":{
        "name": "past",
        "start": now - 2,
        "end": now - 1,
        "span": 5,
        "rank": 1,
    },
    "future":{
        "name": "future",
        "start": now + 3600,
        "end": now + 7200,
        "span": 5,
        "rank": 1,
    },
}

class TestDatabase(object):
    def setup(self):
        d.r.flushdb()

    def test_add(self):
        assert all(d.add(**items["current"]))

    def test_add_twice(self):
        assert all(d.add(**items["current"]))
        assert not any(d.add(**items["current"]))

    def test_rem(self):
        assert all(d.add(**items["current"]))
        assert all(d.rem(items["current"]["name"]))

    def test_rem_nonexistent(self):
        assert not any(d.rem(items["current"]["name"]))
