#!/usr/bin/env python

import json
import os

class Database(object):
    def __init__(self, root="/srv/osmo"):
        self.root = root
