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

    def media_exists(self, name):
        return os.path.isfile(self._cdir("media", name))

    def rem(self, name):
        os.remove(_cdir("media", name))
