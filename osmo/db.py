#!/usr/bin/env python

import os
import osmo.fs
import redis
import time

class Database(object):
    def __init__(self, test=False):
        self.f = osmo.fs.Filesystem()
        self.r = redis.Redis(db=1 if test else 0)

        self.keyspace = "osmo"
        self.rk = {
            "media":    "%s:media"    % self.keyspace,
            "start":    "%s:start"    % self.keyspace,
            "end":      "%s:end"      % self.keyspace,
            "length":   "%s:length"   % self.keyspace,
            "priority": "%s:priority" % self.keyspace,
        }

    def add(self, name, start, end, length, priority):
        p = self.r.pipeline()
        p.sadd(self.rk["media"],    name)
        p.zadd(self.rk["start"],    name, start)
        p.zadd(self.rk["end"],      name, end)
        p.zadd(self.rk["length"],   name, length)
        p.zadd(self.rk["priority"], name, priority)
        return p.execute()

    def rem(self, name):
        p = self.r.pipeline()
        p.srem(self.rk["media"],    name)
        p.zrem(self.rk["start"],    name)
        p.zrem(self.rk["end"],      name)
        p.zrem(self.rk["length"],   name)
        p.zrem(self.rk["priority"], name)
        return p.execute()

    def media_current(self):
        now = int(time.time())
        p = self.r.pipeline()
        p.zrangebyscore(self.rk["start"], "-inf", now)
        p.zrangebyscore(self.rk["end"], now, "+inf")
        return set.intersection(*map(set, p.execute()))

    def media_priority(self, name):
        return self.r.zscore(self.rk["priority"], name)

    def media_length(self, name):
        return self.r.zscore(self.rk["length"], name)

    def current(self):
        return sorted(
            ((x, self.media_length(x)) for x in self.media_current()),
            key=lambda x: self.media_priority(x[0])
        )
