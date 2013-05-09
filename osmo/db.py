#!/usr/bin/env python

import json
import os
import redis
import time

class Database(object):
    def __init__(self, root="/srv/osmo", test=False):
        # Filesystem
        self.root = root
        self.d = { k: os.path.join(self.root, v) for k, v in {
            "media": "media",
            "info": "info",
            "now": "now",
        }.items() }

        # Redis
        self.r = redis.Redis()
        self.keyspace = "osmo"
        self.rk = {
            "start":  "%s:start"  % self.keyspace,
            "end":    "%s:end"    % self.keyspace,
            "length": "%s:length" % self.keyspace,
        }

    def _cdir(self, name, path):
        return os.path.join(self.d[name], path)

    def media_current(self):
        now = int(time.time())
        started =  set(self.r.zrangebyscore(self.rk["start"], "-inf", now))
        notEnded = set(self.r.zrangebyscore(self.rk["end"], now, "+inf"))
        return started & notEnded

    def link_current(self):
        for file_name in self.media_current():
            os.symlink(self._cdir("media", file_name), self._cdir("now"))
