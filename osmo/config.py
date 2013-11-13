#!/usr/bin/env python

"""
Config file loader.
"""

import os
import json


config_file = os.environ["CONFIG_FILE"]
config = json.load(open(config_file))
