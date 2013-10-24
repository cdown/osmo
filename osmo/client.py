#!/usr/bin/env python

"""
Client interface to osmo.

Usage: client.py <media-dir>
"""

from config import config
import sys
import flask
import redis


app = flask.Flask(__name__)
r = redis.Redis(port=config["redis"]["port"])

def event_stream():
    """
    Continually yield the path to the next desired image.

    :returns: a path to the next desired image, in SSE format
    :rtype: generator
    """

    ps = r.pubsub()
    ps.subscribe("osmo")
    for message in ps.listen():
        try:
            data = message["data"].decode("utf8")
        except AttributeError:
            data = message["data"]
        finally:
            yield "data: %s\n\n" % data


@app.route("/stream", methods=["GET"])
def stream():
    """
    The SSE stream, continually yielding paths to the next desired image.

    :returns: an SSE stream of the next desired image
    :rtype: :class:`flask.Response`
    """

    return flask.Response(
        event_stream(),
        mimetype="text/event-stream"
    )


@app.route("/", methods=["GET"])
def home():
    """
    The framework to display images based on the SSE stream.

    :returns: a page that displays images from the SSE stream
    :rtype: :class:`flask.Response`
    """

    return flask.render_template("client.html")


@app.route("/media/<path:name>", methods=["GET"])
def media(name):
    """
    Return a file from the media directory.

    :param name: the file to return
    :returns: a file from the media directory
    :rtype: :class:`flask.Response`
    """

    return flask.send_from_directory(config["paths"]["media_dir"], name)


if __name__ == "__main__":
    app.run(port=config["client"]["port"])
