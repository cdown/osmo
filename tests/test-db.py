#!/usr/bin/env python

import osmo
import tempfile
import shutil

class TestDatabase(object):
    def setup_class(self):
        self.tmpDir = tempfile.mkdtemp(prefix="osmo-nose-")
        self.d = osmo.Database(root=tmpDir)

    def teardown_class(self):
        shutil.rmtree(self.tempDir)
