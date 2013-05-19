#!/usr/bin/env python

import logging
import redis
import time

l = logging.getLogger(__name__)

class Database(object):
    def __init__(self, test=False):
        l.debug("Initialising connection to Redis database.")
        l.debug("Database in test mode? %r" % test)
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
        l.debug("ADD: %s (%d %d %d %d)" % (name, start, end, span, rank))
        p = self.r.pipeline()
        p.sadd(self.rk["items"], name)
        p.zadd(self.rk["start"], name, start)
        p.zadd(self.rk["end"],   name, end)
        p.zadd(self.rk["span"],  name, span)
        p.zadd(self.rk["rank"],  name, rank)
        return p.execute()

    def get(self, name):
        l.debug("GET: %s" % name)
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
        l.debug("REM: %s" % name)
        p = self.r.pipeline()
        p.srem(self.rk["items"], name)
        p.zrem(self.rk["start"], name)
        p.zrem(self.rk["end"],   name)
        p.zrem(self.rk["span"],  name)
        p.zrem(self.rk["rank"],  name)
        return p.execute()

    def current(self):
        l.debug("Getting current items")

        now = int(time.time())
        l.debug("Epoch time: %d" % now)

        p = self.r.pipeline()
        p.zrangebyscore(self.rk["start"], "-inf", now)
        p.zrangebyscore(self.rk["end"], now, "+inf")

        started, not_ended = map(set, p.execute())
        l.debug("Started: %s" % ", ".join(started))
        l.debug("Not ended: %s" % ", ".join(not_ended))

        current_items = set.intersection(started, not_ended)
        l.debug("Intersection: %s" % ", ".join(current_items))

        return sorted(
            current_items,
            key=lambda name: self.rank(name)
        )

    def rank(self, name):
        rank = self.r.zscore(self.rk["rank"], name)
        l.debug("Rank of %s: %d" % (name, rank))
        return rank

    def span(self, name):
        span = self.r.zscore(self.rk["span"], name)
        l.debug("Span of %s: %d" % (name, span))
        return span
