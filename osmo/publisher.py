#!/usr/bin/env python

"""
Publish the currently active slides to Redis.

Usage: publisher.py [options]

Options:
  --help           This help text.
  --test           Use the test Redis database.
  --port PORT      The port to use. [default: 6379]
  --sleep SECONDS  The sleep time when there are no active slides. [default: 5]
"""

from docopt import docopt
import db
import redis
import sys
import time


if __name__ == "__main__":
    args = docopt(__doc__)

    r = redis.Redis(port=int(args["--port"]))
    d = db.Database(test=args["--test"])

    while True:
        active = d.slides_in_state("active")

        if active:
            for name, slide in active:
                print("Published %s, %d seconds" % (name, slide["duration"]))
                r.publish("osmo", name)
                time.sleep(slide["duration"])
        else:
            print("No active slides, sleeping %s seconds" % args["--sleep"])
            r.publish("osmo", "__empty__")
            time.sleep(int(args["--sleep"]))
