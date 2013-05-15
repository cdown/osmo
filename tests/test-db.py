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
        assert d.add(**items["current"]), "Unable to add item"

    def test_add_twice(self):
        assert d.add(**items["current"]), "Unable to add item"
        assert not d.add(**items["current"]), "Succeeded in readding already present item"

    def test_current(self):
        for period in ("current", "past", "future"):
            assert d.add(**items[period]), "Unable to add item: %s" % period

        current_items = d.current()
        assert len(current_items) == 1, "Expected only 1 current item, but got %d" % len(current_items)
        assert current_items[0] == "current", "Got an item which should not be considered current: %s" % current_items[0]

    def test_set_get_same(self):
        inItem = items["current"]
        assert d.add(**inItem), "Unable to add item"
        outItem = d.get(inItem["name"])
        assert inItem == outItem, """Put in "%r", but got "%r" instead""" % (initem, outItem)

    def test_span(self):
        inItem = items["current"]
        inSpan = inItem["span"]
        assert d.add(**inItem), "Unable to add item"
        outSpan = d.span(inItem["name"])
        assert inSpan == outSpan, """Put in span "%d", but got "%d" instead""" % (inSpan, outSpan)

    def test_rank(self):
        inItem = items["current"]
        inRank = inItem["rank"]
        assert d.add(**inItem), "Unable to add item"
        outRank = d.rank(inItem["name"])
        assert inRank == outRank, """Put in rank "%d", but got "%d" instead""" % (inRank, outRank)

    def test_rem(self):
        assert d.add(**items["current"]), "Unable to add item"
        assert d.rem(items["current"]["name"]), "Unable to remove item"

    def test_rem_nonexistent(self):
        assert not d.rem(items["current"]["name"]), "Removed nonexistent item"
