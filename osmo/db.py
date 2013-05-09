#!/usr/bin/env python

import os
import redis
import time

class Database(object):
    def __init__(self, test=False):
        self.r = redis.Redis()
        self.keyspace = "osmo"
        self.rk = {
            "media":  "%s:media"  % self.keyspace,
            "start":  "%s:start"  % self.keyspace,
            "end":    "%s:end"    % self.keyspace,
            "length": "%s:length" % self.keyspace,
        }

    def add(self, name, start, end, length):
        p = self.r.pipeline()
        p.sadd(self.rk["media"],  name)
        p.zadd(self.rk["start"],  name, start)
        p.zadd(self.rk["end"],    name, end)
        p.zadd(self.rk["length"], name, length)
        return p.execute()

    def rem(self, name):
        p = self.r.pipeline()
        p.srem(self.rk["media"],  name)
        p.zrem(self.rk["start"],  name)
        p.zrem(self.rk["end"],    name)
        p.zrem(self.rk["length"], name)
        return p.execute()

    def media_current(self):
        now = int(time.time())
        p = self.r.pipeline()
        p.zrangebyscore(self.rk["start"], "-inf", now)
        p.zrangebyscore(self.rk["end"], now, "+inf")
        return set.intersection(*p.execute())
