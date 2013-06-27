#!/usr/bin/env python

import redis
import time

class Database(object):
    def __init__(self, test=False):
        self.r = redis.Redis(
            db=1 if test else 0,
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
        p = self.r.pipeline()
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
        p.zrem(self.rk["start"],    name)
        p.zrem(self.rk["end"],      name)
        p.zrem(self.rk["duration"], name)
        p.zrem(self.rk["rank"],     name)
        return p.execute()

    def get_state(self, state="active"):
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
        elif state == "any":
            items = self.r.zrangebyscore(self.rk["start"], "-inf", "+inf")
        else:
            raise NotImplementedError("Unknown state: %s" % state)

        durations = [ (name, self.duration(name)) for name in items ]
        return sorted(
            durations,
            key=lambda duration: self.rank(duration[0]),
        )

    def rank(self, name):
        return self.r.zscore(self.rk["rank"], name)

    def duration(self, name):
        return self.r.zscore(self.rk["duration"], name)
