#!/usr/bin/env python

import osmo
import tempfile
import shutil

class TestDatabase(object):
    def setup_class(self):
        self.temp_dir = tempfile.mkdtemp(prefix="osmo-nose-")
        self.d = osmo.Database(root=temp_dir)

    def teardown_class(self):
        shutil.rmtree(self.tempDir)
