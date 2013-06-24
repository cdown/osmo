#!/usr/bin/env python

import db
import redis
import time

r = redis.Redis()
d = db.Database()

if __name__ == "__main__":
    while True:
        current = d.current()
        if not current:
            time.sleep(5)
            continue

        for name, span in d.current():
            r.publish("osmo", name)
            time.sleep(span)
