#!/usr/bin/env python

import os
import osmo.db

class Filesystem(object):
    def __init__(self, root="/srv/osmo", test=False):
        self.root = root
        self.d = { k: os.path.join(self.root, v) for k, v in {
            "media": "media",
            "now": "now",
        }.items() }

    def _cdir(self, name, path):
        return os.path.join(self.d[name], path)

    def link_current(self):
        for file_name in self.db.media_current():
            os.symlink(self._cdir("media", file_name), self._cdir("now"))
