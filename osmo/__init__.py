#!/usr/bin/env python

from .db import Database as _d
from .fs import Filesystem as _f

_d = _d()
_f = _f()

def add(name, start, end, length):
    _d.add(name, start, end, length)

def rem(name):
    _d.rem(name)
    _f.rem(name)

def current():
    return _d.current()
