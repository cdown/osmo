#!/usr/bin/env python

import redis
import time

class Database(object):
    def __init__(self, test=False):
        self.r = redis.Redis(db=1 if test else 0, decode_responses=True)
        self.keyspace = "osmo"
        self.rk = {
            "items": "%s:items" % self.keyspace,
            "start": "%s:start" % self.keyspace,
            "end":   "%s:end"   % self.keyspace,
            "span":  "%s:span"  % self.keyspace,
            "rank":  "%s:rank"  % self.keyspace,
        }

    def add(self, name, start, end, span, rank):
        p = self.r.pipeline()
        p.sadd(self.rk["items"], name)
        p.zadd(self.rk["start"], name, start)
        p.zadd(self.rk["end"],   name, end)
        p.zadd(self.rk["span"],  name, span)
        p.zadd(self.rk["rank"],  name, rank)
        return all(p.execute())

    def get(self, name):
        p = self.r.pipeline()
        p.zscore(self.rk["start"], name)
        p.zscore(self.rk["end"],   name)
        p.zscore(self.rk["span"],  name)
        p.zscore(self.rk["rank"],  name)
        start, end, span, rank = p.execute()
        return {
            "name": name,
            "start": start,
            "end": end,
            "span": span,
            "rank": rank,
        }

    def rem(self, name):
        p = self.r.pipeline()
        p.srem(self.rk["items"], name)
        p.zrem(self.rk["start"], name)
        p.zrem(self.rk["end"],   name)
        p.zrem(self.rk["span"],  name)
        p.zrem(self.rk["rank"],  name)
        return all(p.execute())

    def current(self):
        now = int(time.time())
        p = self.r.pipeline()
        p.zrangebyscore(self.rk["start"], "-inf", now)
        p.zrangebyscore(self.rk["end"], now, "+inf")
        current_items = set.intersection(*map(set, p.execute()))
        return sorted(
            current_items,
            key=lambda name: self.get_rank(name)
        )

    def get_rank(self, name):
        return self.r.zscore(self.rk["rank"], name)

    def get_span(self, name):
        return self.r.zscore(self.rk["span"], name)
