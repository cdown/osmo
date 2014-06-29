#!/usr/bin/env python

from config import config
import db
import sys
import redis
import time


if __name__ == "__main__":
    r = redis.Redis(port=config["redis"]["port"])
    d = db.Database()

    while True:
        active = d.slides_in_state("active")

        if active:
            for name, slide in active:
                print("Published %s, %d seconds" % (name, slide["duration"]))
                sys.stdout.flush()
                r.publish("osmo", name)
                time.sleep(slide["duration"])
        else:
            sleep_time = config["publisher"]["empty_sleep"]
            print("No active slides, sleeping %d seconds" % sleep_time)
            sys.stdout.flush()
            r.publish("osmo", "__empty__")
            time.sleep(sleep_time)
