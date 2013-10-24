#!/usr/bin/env python

"""
Database functions.
"""

import datetime
import redis
import time
try:
    from .config import config
except SystemError:  # Not being used in larger osmo context
    from config import config


class Database(object):
    def __init__(self):
        """
        Initialise the Redis backend, and populate the key names.
        """

        self.r = redis.Redis(
            port=config["redis"]["port"],
            decode_responses=True,
        )
        self.keyspace = "osmo"
        self.rk = {
            "start":    "%s:start"    % self.keyspace,
            "end":      "%s:end"      % self.keyspace,
            "duration": "%s:duration" % self.keyspace,
            "rank":     "%s:rank"     % self.keyspace,
        }

    def add(self, name, start, end, duration, rank):
        """
        Add a slide.

        :param name: the slide name
        :param start: when the slide should become part of the queue
        :param end: when the slide should leave the queue
        :param duration: the duration to display the slide in one queue loop
        :param rank: the rank/priority of display
        :returns: the success of each Redis pipeline call
        :rtype: a list of bools
        """

        p = self.r.pipeline()
        p.zadd(self.rk["start"],    name, start)
        p.zadd(self.rk["end"],      name, end)
        p.zadd(self.rk["duration"], name, duration)
        p.zadd(self.rk["rank"],     name, rank)
        return p.execute()

    def get(self, name):
        """
        Return the metadata for a slide.

        :param name: the slide name
        :returns: slide attributes
        :rtype: dict
        """

        p = self.r.pipeline()
        p.zscore(self.rk["start"],    name)
        p.zscore(self.rk["end"],      name)
        p.zscore(self.rk["duration"], name)
        p.zscore(self.rk["rank"],     name)
        start, end, duration, rank = p.execute()
        return {
            "name": name,
            "start": start,
            "end": end,
            "duration": duration,
            "rank": rank,
        }

    def remove(self, name):
        """
        Remove a slide.

        :param name: the slide name
        :returns: the success of each Redis pipeline call
        :rtype: a list of bools
        """

        p = self.r.pipeline()
        p.zrem(self.rk["start"],    name)
        p.zrem(self.rk["end"],      name)
        p.zrem(self.rk["duration"], name)
        p.zrem(self.rk["rank"],     name)
        return p.execute()

    def slides_in_state(self, state="active", sort="rank"):
        """
        Return information about all the slides in a state.

        :param state: which state to return slides for
        :param sort: the info key to sort the slides by
        :type sort: str or None
        :returns: attributes of all slides in this state, sorted by `sort`
        :rtype: a list of tuples
        """

        now = time.time()

        if state == "active":
            p = self.r.pipeline()
            p.zrangebyscore(self.rk["start"], "-inf", now)
            p.zrangebyscore(self.rk["end"], now, "+inf")
            started, not_ended = map(set, p.execute())
            slides = started & not_ended
        elif state == "future":
            slides = self.r.zrangebyscore(self.rk["start"], now + 1, "+inf")
        elif state == "past":
            slides = self.r.zrangebyscore(self.rk["end"], "-inf", now - 1)
        elif state == "all":
            slides = self.r.zrangebyscore(self.rk["start"], "-inf", "+inf")
        else:
            raise NotImplementedError("Unknown state: %s" % state)

        info = []

        for name in slides:
            info.append((name, self.info(name)))

        if sort is not None:
            info.sort(key=lambda x: x[1][sort])

        return info

    def info(self, name):
        """
        Return information about a slide.

        :param name: the slide name
        :returns: information about the slide
        :rtype: dict
        """

        p = self.r.pipeline()
        p.zscore(self.rk["rank"], name)
        p.zscore(self.rk["duration"], name)
        p.zscore(self.rk["start"], name)
        p.zscore(self.rk["end"], name)
        rank, duration, start, end = p.execute()

        return {
            "rank": rank,
            "duration": duration,
            "start": start,
            "end": end,
        }
