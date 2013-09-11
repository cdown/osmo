#!/usr/bin/env python

"""
Database functions.
"""

import datetime
import redis
import time


class Database(object):
    def __init__(self, test=False):
        """
        Initialise the Redis backend, and populate the key names.

        :param test: whether to use the test database or not
        """

        self.r = redis.Redis(
            port=6379 if not test else 28692,
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
        :return: a list, where all elements will evaluate to True if each
                 call executed correctly
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
        :return: a dict containing slide information
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

    def rem(self, name):
        """
        Remove a slide.

        :param name: the slide name
        :return: a list, where all elements will evaluate to True if each
                 call executed correctly
        """

        p = self.r.pipeline()
        p.zrem(self.rk["start"],    name)
        p.zrem(self.rk["end"],      name)
        p.zrem(self.rk["duration"], name)
        p.zrem(self.rk["rank"],     name)
        return p.execute()

    def get_all_metadata(self):
        """
        Return a generator with information about all slides.
        """

        names = self.r.zrangebyscore(self.rk["start"], "-inf", "+inf")
        for name in names:
            yield {
                "name": name,
                "duration": int(self.duration(name)),
                "start": self.start(name),
                "end": self.end(name),
                "rank": int(self.rank(name)),
            }

    def get_state(self, state="active"):
        """
        Return the names of all slides in a state.

        :param state: which state to return slides for
        :returns: the names of all slides in this state
        """

        now = time.time()

        if state == "active":
            p = self.r.pipeline()
            p.zrangebyscore(self.rk["start"], "-inf", now)
            p.zrangebyscore(self.rk["end"], now, "+inf")
            started, not_ended = map(set, p.execute())
            items = started & not_ended
        elif state == "future":
            items = self.r.zrangebyscore(self.rk["start"], now + 1, "+inf")
        elif state == "past":
            items = self.r.zrangebyscore(self.rk["end"], "-inf", now - 1)
        elif state == "all":
            items = self.r.zrangebyscore(self.rk["start"], "-inf", "+inf")
        else:
            raise NotImplementedError("Unknown state: %s" % state)

        durations = [(name, self.duration(name)) for name in items]
        return sorted(
            durations,
            key=lambda duration: self.rank(duration[0]),
        )

    def rank(self, name):
        """
        Return the rank of a slide.

        :param name: the slide name
        :returns: the slide rank
        """

        return self.r.zscore(self.rk["rank"], name)

    def duration(self, name):
        """
        Return the duration of a slide.

        :param name: the slide name
        :returns: the slide duration
        """

        return self.r.zscore(self.rk["duration"], name)

    def start(self, name):
        """
        Return the start time of a slide.

        :param name: the slide name
        :returns: the slide start time
        """

        return datetime.datetime.fromtimestamp(
            self.r.zscore(self.rk["start"], name)
        )

    def end(self, name):
        """
        Return the end time of a slide.

        :param name: the slide name
        :returns: the slide end time
        """

        return datetime.datetime.fromtimestamp(
            self.r.zscore(self.rk["end"], name)
        )
