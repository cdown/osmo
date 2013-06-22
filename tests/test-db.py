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
        assert all(d.add(**items["current"])), "Unable to add item"

    def test_add_twice(self):
        assert all(d.add(**items["current"])), "Unable to add item"
        assert not any(d.add(**items["current"])), "Succeeded in readding already present item"

    def test_current(self):
        for period in ("current", "past", "future"):
            assert all(d.add(**items[period])), "Unable to add item: %s" % period

        current_items = d.current()
        assert len(current_items) == 1, "Expected only 1 current item, but got %d" % len(current_items)
        assert len(current_items[0]) == 2, "Expected 2-tuple item, but got %d" % len(current_items[0])
        assert current_items[0][0] == "current", "Got an item which should not be considered current: %s" % current_items[0]

    def test_set_get_same(self):
        item_in = items["current"]
        assert all(d.add(**item_in)), "Unable to add item"
        item_out = d.get(item_in["name"])
        assert item_in == item_out, """Put in "%r", but got "%r" instead""" % (item_in, item_out)

    def test_span(self):
        item_in = items["current"]
        span_in = item_in["span"]
        assert all(d.add(**item_in)), "Unable to add item"
        span_out = d.span(item_in["name"])
        assert span_in == span_out, """Put in span "%d", but got "%d" instead""" % (span_in, span_out)

    def test_rank(self):
        item_in = items["current"]
        rank_in = item_in["rank"]
        assert all(d.add(**item_in)), "Unable to add item"
        rank_out = d.rank(item_in["name"])
        assert rank_in == rank_out, """Put in rank "%d", but got "%d" instead""" % (rank_in, rank_out)

    def test_rem(self):
        assert all(d.add(**items["current"])), "Unable to add item"
        assert all(d.rem(items["current"]["name"])), "Unable to remove item"

    def test_rem_nonexistent(self):
        assert not any(d.rem(items["current"]["name"])), "Removed nonexistent item"
