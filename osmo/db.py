#!/usr/bin/env python

import json
import os
import redis

class Database(object):
    def __init__(self, root="/srv/osmo", test=False):
        # Filesystem
        self.root = root
        self.d = { k: os.path.join(self.root, v) for k, v in {
            "media":"media",
            "info":"info",
        }.items() }

        # Redis
        self.r = redis.Redis()
        self.keyspace = "osmo"
        self.rk = {
            "start":  "%s:start"  % self.keyspace,
            "end":    "%s:end"    % self.keyspace,
            "length": "%s:length" % self.keyspace,
        }
