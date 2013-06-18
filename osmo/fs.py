#!/usr/bin/env python

import os
import shutil
import tempfile

class Filesystem(object):
    def __init__(self, root="/srv/osmo"):
        self.root = root
        self.d = { k: os.path.join(self.root, v) for k, v in {
            "media": "media",
        }.items() }

    def _cdir(self, name, path):
        return os.path.join(self.d[name], path)

    def media(self, name):
        return open(self._cdir("media", name), "rb")

    def rem(self, name):
        os.remove(self._cdir("media", name))
