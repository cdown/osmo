#!/usr/bin/env python

import os

def _listdir_full(path):
    return { os.path.join(path, fn) for fn in os.listdir(path) }
