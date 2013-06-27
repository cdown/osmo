#!/usr/bin/env python

import osmo.db
import time

d = osmo.db.Database(test=True)
now = time.time()
items = {
    "active":{
        "name": "active",
        "start": now - 1,
        "end": now + 3600,
        "duration": 5,
        "rank": 1,
    },
    "past":{
        "name": "past",
        "start": now - 2,
        "end": now - 1,
        "duration": 5,
        "rank": 1,
    },
    "future":{
        "name": "future",
        "start": now + 3600,
        "end": now + 7200,
        "duration": 5,
        "rank": 1,
    },
}

class TestDatabase(object):
    def setup(self):
        d.r.flushdb()

    def teardown(self):
        d.r.flushdb()

    def test_add(self):
        assert all(d.add(**items["active"])), "Unable to add item"

    def test_add_twice(self):
        assert all(d.add(**items["active"])), "Unable to add item"
        assert not any(d.add(**items["active"])), "Succeeded in readding already present item"

    def test_active(self):
        for period in ("active", "past", "future"):
            assert all(d.add(**items[period])), "Unable to add item: %s" % period

        active_items = d.active()
        assert len(active_items) == 1, "Expected only 1 active item, but got %d" % len(active_items)
        assert len(active_items[0]) == 2, "Expected 2-tuple item, but got %d" % len(active_items[0])
        assert active_items[0][0] == "active", "Got an item which should not be considered active: %s" % active_items[0]

    def test_set_get_same(self):
        item_in = items["active"]
        assert all(d.add(**item_in)), "Unable to add item"
        item_out = d.get(item_in["name"])
        assert item_in == item_out, """Put in "%r", but got "%r" instead""" % (item_in, item_out)

    def test_duration(self):
        item_in = items["active"]
        duration_in = item_in["duration"]
        assert all(d.add(**item_in)), "Unable to add item"
        duration_out = d.duration(item_in["name"])
        assert duration_in == duration_out, """Put in duration "%d", but got "%d" instead""" % (duration_in, duration_out)

    def test_rank(self):
        item_in = items["active"]
        rank_in = item_in["rank"]
        assert all(d.add(**item_in)), "Unable to add item"
        rank_out = d.rank(item_in["name"])
        assert rank_in == rank_out, """Put in rank "%d", but got "%d" instead""" % (rank_in, rank_out)

    def test_rem(self):
        assert all(d.add(**items["active"])), "Unable to add item"
        assert all(d.rem(items["active"]["name"])), "Unable to remove item"

    def test_rem_nonexistent(self):
        assert not any(d.rem(items["active"]["name"])), "Removed nonexistent item"
