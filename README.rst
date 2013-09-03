osmo
====

**osmo** is a digital signage framework for minimalists. It doesn't provide you
with anything fancy, just a web interface to upload images to display, and a
client to display them with.

The client can run anywhere there is a web browser that supports SSE -- it
doesn't require any installation.

Testing
_______

.. image:: https://travis-ci.org/cdown/osmo.png?branch=master
    :target: https://travis-ci.org/cdown/osmo

::

    $ pip install nose
    $ tests/run
    .............
    ----------------------------------------------------------------------
    Ran 13 tests in 11.926s

    OK

License
-------

osmo is MIT licensed. See `the LICENSE file
<https://github.com/cdown/osmo/blob/master/LICENSE>`__ for full details.
