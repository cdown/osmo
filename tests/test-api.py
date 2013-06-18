#!/usr/bin/env python

import osmo.db
import time
import json
import os

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

d = osmo.db.Database(test=True)
now = time.time()
items = {
    "current":{
        "name": "current.jpg",
        "start": now - 1,
        "end": now + 3600,
        "span": 5,
        "rank": 1,
    },
    "past":{
        "name": "past.jpg",
        "start": now - 2,
        "end": now - 1,
        "span": 5,
        "rank": 1,
    },
    "future":{
        "name": "future.jpg",
        "start": now + 3600,
        "end": now + 7200,
        "span": 5,
        "rank": 1,
    },
}

def _at_script_dir(path):
    return os.path.join(os.path.dirname(__file__), path)

d.r.flushdb()
for period in ("current", "past", "future"):
    assert all(d.add(**items[period])), "Unable to add item: %s" % period

class TestAPI(object):
    def test_items(self):
        res = urlopen("http://localhost:8080/current")
        res_json = json.loads(res.read().decode("utf8"))
        assert res_json == { "items": [ "current.jpg" ] }, res_json

    def test_media(self):
        media_dir = _at_script_dir("media")
        res = urlopen("http://localhost:8080/media/current.jpg").read()
        with open(os.path.join(media_dir, "current.jpg"), "rb") as f:
            assert res == f.read()
