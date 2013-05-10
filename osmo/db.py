#!/usr/bin/env python

import redis
import time

class Database(object):
    def __init__(self, test=False):
        self.r = redis.Redis(db=1 if test else 0, decode_responses=True)
        self.keyspace = "osmo"
        self.rk = {
            "media": "%s:media" % self.keyspace,
            "start": "%s:start" % self.keyspace,
            "end":   "%s:end"   % self.keyspace,
            "span":  "%s:span"  % self.keyspace,
            "rank":  "%s:rank"  % self.keyspace,
        }

    def add(self, name, start, end, span, rank):
        p = self.r.pipeline()
        p.sadd(self.rk["media"], name)
        p.zadd(self.rk["start"], name, start)
        p.zadd(self.rk["end"],   name, end)
        p.zadd(self.rk["span"],  name, span)
        p.zadd(self.rk["rank"],  name, rank)
        return p.execute()

    def rem(self, name):
        p = self.r.pipeline()
        p.srem(self.rk["media"], name)
        p.zrem(self.rk["start"], name)
        p.zrem(self.rk["end"],   name)
        p.zrem(self.rk["span"],  name)
        p.zrem(self.rk["rank"],  name)
        return p.execute()

    def current(self):
        now = int(time.time())
        p = self.r.pipeline()
        p.zrangebyscore(self.rk["start"], "-inf", now)
        p.zrangebyscore(self.rk["end"], now, "+inf")
        current_media = set.intersection(*map(set, p.execute()))
        return sorted(
            (x for x in current_media),
            key=lambda name: self.media_rank(name)
        )

    def media_rank(self, name):
        return self.r.zscore(self.rk["rank"], name)

    def media_span(self, name):
        return self.r.zscore(self.rk["span"], name)
