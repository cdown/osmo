#!/usr/bin/env python

import os

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

def _at_script_dir(path):
    return os.path.join(os.path.dirname(__file__), path)

def test_media():
    media_dir = _at_script_dir("media")

    for filename in os.listdir(media_dir):
        res = urlopen("http://localhost:8000/media/%s" % filename).read()
        with open(os.path.join(media_dir, filename), "rb") as f:
            assert res == f.read()
