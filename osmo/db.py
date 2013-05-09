#!/usr/bin/env python

import os
import redis
import time

class Database(object):
    def __init__(self, test=False):
        self.r = redis.Redis()
        self.keyspace = "osmo"
        self.rk = {
            "start":  "%s:start"  % self.keyspace,
            "end":    "%s:end"    % self.keyspace,
            "length": "%s:length" % self.keyspace,
        }

    def add(self, name, start, end, length):
        p = self.r.pipeline()
        p.zadd(self.rk["start"],  name, start)
        p.zadd(self.rk["end"],    name, end)
        p.zadd(self.rk["length"], name, length)
        return p.execute()

    def rem(self, name):
        p = self.r.pipeline()
        p.zrem(self.rk["start"],  name)
        p.zrem(self.rk["end"],    name)
        p.zrem(self.rk["length"], name)
        return p.execute()

    def media_current(self):
        now = int(time.time())
        started =  set(self.r.zrangebyscore(self.rk["start"], "-inf", now))
        notEnded = set(self.r.zrangebyscore(self.rk["end"], now, "+inf"))
        return started & notEnded
