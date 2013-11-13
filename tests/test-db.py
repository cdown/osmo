#!/usr/bin/env python

import osmo.db
import time

d = osmo.db.Database()
now = time.time()
slides = {
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

def _add_all():
    for period in ("active", "past", "future"):
        assert all(d.add(**slides[period])), "Unable to add slide: %s" % period

class TestDatabase(object):
    def setup(self):
        d.r.flushdb()

    def teardown(self):
        d.r.flushdb()

    def test_add(self):
        assert all(d.add(**slides["active"])), "Unable to add slide"

    def test_add_twice(self):
        assert all(d.add(**slides["active"])), "Unable to add slide"
        assert not any(d.add(**slides["active"])), "Succeeded in readding already present slide"

    def test_active(self):
        _add_all()
        my_slides = d.slides_in_state("active")
        assert len(my_slides) == 1, "Expected 1 active slide, but got %d" % len(my_slides)
        assert len(my_slides[0]) == 2, "Expected 2-tuple slide, but got %d" % len(my_slides[0])
        assert my_slides[0][0] == "active", "Got an slide which should not be considered active: %s" % my_slides[0]

    def test_past(self):
        _add_all()
        my_slides = d.slides_in_state("past")
        assert len(my_slides) == 1, "Expected 1 past slide, but got %d" % len(my_slides)
        assert len(my_slides[0]) == 2, "Expected 2-tuple slide, but got %d" % len(my_slides[0])
        assert my_slides[0][0] == "past", "Got an slide which should not be considered past: %s" % my_slides[0]

    def test_future(self):
        _add_all()
        my_slides = d.slides_in_state("future")
        assert len(my_slides) == 1, "Expected 1 future slide, but got %d" % len(my_slides)
        assert len(my_slides[0]) == 2, "Expected 2-tuple slide, but got %d" % len(my_slides[0])
        assert my_slides[0][0] == "future", "Got an slide which should not be considered future: %s" % my_slides[0]

    def test_all(self):
        _add_all()
        my_slides = d.slides_in_state("all")
        assert len(my_slides) == 3, "Expected 3 slides, but got %d" % len(my_slides)
        assert len(my_slides[0]) == 2, "Expected 2-tuple slide, but got %d" % len(my_slides[0])

    def test_set_get_same(self):
        slide_in = slides["active"]
        assert all(d.add(**slide_in)), "Unable to add slide"
        slide_out = d.get(slide_in["name"])
        assert slide_in == slide_out, """Put in "%r", but got "%r" instead""" % (slide_in, slide_out)

    def test_duration(self):
        slide_in = slides["active"]
        duration_in = slide_in["duration"]
        assert all(d.add(**slide_in)), "Unable to add slide"
        duration_out = d.info(slide_in["name"])["duration"]
        assert duration_in == duration_out, """Put in duration "%d", but got "%d" instead""" % (duration_in, duration_out)

    def test_rank(self):
        slide_in = slides["active"]
        rank_in = slide_in["rank"]
        assert all(d.add(**slide_in)), "Unable to add slide"
        rank_out = d.info(slide_in["name"])["rank"]
        assert rank_in == rank_out, """Put in rank "%d", but got "%d" instead""" % (rank_in, rank_out)

    def test_rem(self):
        assert all(d.add(**slides["active"])), "Unable to add slide"
        assert all(d.remove(slides["active"]["name"])), "Unable to remove slide"

    def test_rem_nonexistent(self):
        assert not any(d.remove(slides["active"]["name"])), "Removed nonexistent slide"
