#!/usr/bin/env python

import json
import os

class Database(object):
    def __init__(self, root="/srv/osmo"):
        self.root = root
        self.d = { k: os.path.join(self.root, v) for k, v in {
            "media":"media",
            "info":"info",
            "current":"current",
        }.items() }
