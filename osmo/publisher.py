#!/usr/bin/env python

import db
import redis
import time

r = redis.Redis()
d = db.Database()

if __name__ == "__main__":
    while True:
        active = d.get_state(state="active")
        if not active:
            print("No active items, sleeping for 5 seconds")
            time.sleep(5)
            continue

        for name, duration in active:
            print("Publishing %s, sleeping for %d seconds" % (name, duration))
            r.publish("osmo", name)
            time.sleep(duration)
