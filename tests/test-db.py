#!/usr/bin/env python

import osmo
import tempfile

tmpDir = tempfile.mkdtemp(prefix="osmo-nose-")
d = osmo.Database(root=tmpDir)
