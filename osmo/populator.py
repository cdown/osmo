#!/usr/bin/env python

import osmo.db
import redis
import time

r = redis.Redis()
d = osmo.db.Database()

if __name__ == "__main__":
    while True:
        for name, span in d.current():
            r.publish("osmo", name)
            time.sleep(span)
