#!/usr/bin/env python

import sys

sys.path.append(".")

from osmo.config import config

for key in sys.argv[1:]:
    config = config[key]

print(config)
