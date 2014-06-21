#!/usr/bin/env python

import osmo.admin
from osmo.config import config


def test_allowed_file_bad():
    assert not any(
        osmo.admin._allowed_file("foo.%sx" % ext)
        for ext in config["admin"]["valid_extensions"]
    )


def test_allowed_file_good():
    assert all(
        osmo.admin._allowed_file("foo.%s" % ext)
        for ext in config["admin"]["valid_extensions"]
    )

def test_allowed_file_case():
    assert all(
        osmo.admin._allowed_file("foo.%s" % ext.title())
        for ext in config["admin"]["valid_extensions"]
    )
