#!/usr/bin/env python

import osmo.db
import time
import json

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

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

d.r.flushdb()
for period in ("current", "past", "future"):
    assert all(d.add(**items[period])), "Unable to add item: %s" % period

class TestAPI(object):
    def test_items(self):
        res = urlopen("http://localhost:8080/current")
        res_json = json.loads(res.read().decode("utf8"))
        assert res_json == { "items": [ "current" ] }
