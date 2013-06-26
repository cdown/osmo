#!/usr/bin/env python

import redis
import time

class Database(object):
    def __init__(self, test=False):
        self.r = redis.Redis(
            db = 1 if test else 0,
            decode_responses = True,
        )
        self.keyspace = "osmo"
        self.rk = {
            "items":    "%s:items"    % self.keyspace,
            "start":    "%s:start"    % self.keyspace,
            "end":      "%s:end"      % self.keyspace,
            "duration": "%s:duration" % self.keyspace,
            "rank":     "%s:rank"     % self.keyspace,
        }

    def add(self, name, start, end, duration, rank):
        p = self.r.pipeline()
        p.sadd(self.rk["items"],    name)
        p.zadd(self.rk["start"],    name, start)
        p.zadd(self.rk["end"],      name, end)
        p.zadd(self.rk["duration"], name, duration)
        p.zadd(self.rk["rank"],     name, rank)
        return p.execute()

    def get(self, name):
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
        p = self.r.pipeline()
        p.srem(self.rk["items"],    name)
        p.zrem(self.rk["start"],    name)
        p.zrem(self.rk["end"],      name)
        p.zrem(self.rk["duration"], name)
        p.zrem(self.rk["rank"],     name)
        return p.execute()

    def current(self):
        now = int(time.time())

        p = self.r.pipeline()
        p.zrangebyscore(self.rk["start"], "-inf", now)
        p.zrangebyscore(self.rk["end"], now, "+inf")
        started, not_ended = map(set, p.execute())

        current_items = started & not_ended
        current_durations = [ (name, self.duration(name)) for name in current_items ]

        return sorted(
            current_durations,
            key=lambda duration: self.rank(duration[0]),
        )

    def rank(self, name):
        return self.r.zscore(self.rk["rank"], name)

    def duration(self, name):
        return self.r.zscore(self.rk["duration"], name)
