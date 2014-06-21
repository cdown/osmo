#!/usr/bin/env python

import osmo.admin


def test_allowed_file():
    assert osmo.admin._allowed_file("foo.bar") == False
    assert osmo.admin._allowed_file("foo.jpg") == True
