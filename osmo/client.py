#!/usr/bin/env python

import osmo.db
import osmo.fs

d = osmo.db.Database()
f = osmo.fs.Filesystem()

def add(name, start, end, length):
    d.add(name, start, end, length)

def rem(name):
    d.rem(name)
    f.rem(name)
