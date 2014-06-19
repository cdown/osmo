#!/usr/bin/env python

from config import config
import db
import redis
import sys
import time


if __name__ == "__main__":
    r = redis.Redis(port=config["redis"]["port"])
    d = db.Database()

    while True:
        active = d.slides_in_state("active")

        if active:
            for name, slide in active:
                sys.stdout.write("Published %s, %d seconds\n" % (name, slide["duration"]))
                sys.stdout.flush()
                r.publish("osmo", name)
                time.sleep(slide["duration"])
        else:
            sleep_time = config["publisher"]["empty_sleep"]
            sys.stdout.write("No active slides, sleeping %d seconds\n" % sleep_time)
            sys.stdout.flush()
            r.publish("osmo", "__empty__")
            time.sleep(sleep_time)
