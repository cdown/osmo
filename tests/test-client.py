#!/usr/bin/env python

import os
import osmo.db
import sseclient
import time

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


d = osmo.db.Database(test=True)
now = time.time()
items = {
    "active1":{
        "name": "active1",
        "start": now - 1,
        "end": now + 3600,
        "duration": 1,
        "rank": 10,
    },
    "active2":{
        "name": "active2",
        "start": now - 1,
        "end": now + 3600,
        "duration": 2,
        "rank": 2,
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

def _add_all():
    for period in items.keys():
        assert all(d.add(**items[period])), "Unable to add item: %s" % period

def _at_script_dir(path):
    return os.path.join(os.path.dirname(__file__), path)

class TestClient(object):
    def setup(self):
        d.r.flushdb()

    def teardown(self):
        d.r.flushdb()

    def test_media(stream):
        media_dir = _at_script_dir("media")

        for filename in os.listdir(media_dir):
            res = urlopen("http://localhost:8000/media/%s" % filename).read()
            with open(os.path.join(media_dir, filename), "rb") as f:
                assert res == f.read()

    def test_stream(stream):
        last_time = None
        last_item = None
        started = False

        stream = sseclient.SSEClient("http://localhost:8000/stream")

        _add_all()

        i = 0
        for message in stream:
            if not started and message.data == "1":
                # Stream is ready to send data
                started = True
                continue

            assert started, "Expected first event to be Redis subscription acknowledgement, but got %s" % message.data

            current_time = time.time()

            if i % 2 == 0:
                assert message.data == "active2"
            else:
                assert message.data == "active1"

            if last_item:
                print(round(current_time - last_time))
                print(items[last_item]["duration"])
                print(current_time)
                print(last_time)
                assert round(current_time - last_time) == items[last_item]["duration"]

            last_time = current_time
            last_item = message.data

            if i > 5:
                break

            i += 1
