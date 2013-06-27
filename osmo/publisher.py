#!/usr/bin/env python

import db
import redis
import time

r = redis.Redis()
d = db.Database()

if __name__ == "__main__":
    while True:
        active = d.active()
        if not active:
            time.sleep(5)
            continue

        for name, duration in d.active():
            r.publish("osmo", name)
            time.sleep(duration)
