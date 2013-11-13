osmo
====

**osmo** is a digital signage framework for minimalists. It doesn't provide you
with anything fancy, just a web interface to upload images to display, and a
client to display them with.

The client can run anywhere there is a web browser that supports SSE -- it
doesn't require any installation.

Running
-------

For now, take a look at
`tests/run
<https://github.com/cdown/osmo/blob/master/tests/run>`__, but in
essence:

- Run the publisher (publisher.py)
- Run the admin interface (admin.py, optional, for adding slides)
- Run the SSE application (client.py)
- Point your browser at wherever you're serving the client.

You'll want to use gunicorn or another multithreaded server if you plan on
having more than one client.

Redis
-----

Since all critical multi-stage operations are done in a pipeline, it's pretty
hard to make the database become inconsistent, so you shouldn't worry too much
about that.

The only real thing to worry about is that Redis data is flushed to disk often
enough to not worry about it. My recommendations would to use an AOF redo log,
and persist to disk every few minutes (and configure it to snapshot every now
and then in case someone clears the DB because they have a vendetta against
your slides).

Testing
_______

.. image:: https://travis-ci.org/cdown/osmo.png?branch=master
    :target: https://travis-ci.org/cdown/osmo

::

    $ pip install -r requirements.txt
    [...]
    $ pip install -r requirements-dev.txt
    [...]
    $ tests/run
    .............
    ----------------------------------------------------------------------
    Ran 13 tests in 11.926s

    OK

License
-------

osmo is MIT licensed. See `the LICENSE file
<https://github.com/cdown/osmo/blob/master/LICENSE>`__ for full details.
