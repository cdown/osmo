#!/usr/bin/env python

import os
import osmo.db
import shutil

class Filesystem(object):
    def __init__(self, root="/srv/osmo", test=False):
        self.root = root
        self.d = { k: os.path.join(self.root, v) for k, v in {
            "media": "media",
        }.items() }

    def _cdir(self, name, path):
        return os.path.join(self.d[name], path)

    def add(self, path):
        shutil.copy(path, self._cdir("media"))

    def rem(self, file_name):
        os.remove(_cdir("media", file_name))
