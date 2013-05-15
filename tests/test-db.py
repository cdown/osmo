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

    def teardown(self):
        d.r.flushdb()

    def test_add(self):
        assert d.add(**items["current"])

    def test_add_twice(self):
        assert d.add(**items["current"])
        assert not d.add(**items["current"])

    def test_current(self):
        assert d.add(**items["current"])
        assert d.add(**items["past"])
        assert d.add(**items["future"])

        current = d.current()
        assert len(current) == 1
        assert current[0] == "current"

    def test_set_get_same(self):
        inItem = items["current"]
        assert d.add(**inItem)
        outItem = d.get(inItem["name"])
        assert inItem == outItem

    def test_span(self):
        item = items["current"]
        assert d.add(**item)
        assert d.get_span(item["name"]) == item["span"]

    def test_rank(self):
        item = items["current"]
        assert d.add(**item)
        assert d.get_rank(item["name"]) == item["rank"]

    def test_rem(self):
        assert d.add(**items["current"])
        assert d.rem(items["current"]["name"])

    def test_rem_nonexistent(self):
        assert not d.rem(items["current"]["name"])
