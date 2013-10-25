#!/usr/bin/env python

import os
import osmo.db
import sseclient
import time

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


d = osmo.db.Database()
now = time.time()
slides = {
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
    for period in slides.keys():
        assert all(d.add(**slides[period])), "Unable to add slide: %s" % period

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
        last_slide = None
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
                assert message.data == "active2", "Expected active2, got %s" % message.data
            else:
                assert message.data == "active1", "Expected active1, got %s" % message.data

            if last_slide:
                print(round(current_time - last_time))
                print(slides[last_slide]["duration"])
                print(current_time)
                print(last_time)
                assert round(current_time - last_time) == slides[last_slide]["duration"]

            last_time = current_time
            last_slide = message.data

            if i > 5:
                break

            i += 1
