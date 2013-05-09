#!/usr/bin/env python

import osmo.db
import time

d = osmo.db.Database()

def run():
    while True:
        for media in d.media_current():
            length = d.media_length(media)
            print("%s, duration %d" % (media, length))
            time.sleep(length)
