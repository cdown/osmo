#!/usr/bin/env python

"""
Client interface.
"""

import sys
import flask
import redis
import argparse


app = flask.Flask(__name__)
r = redis.Redis()

# This is only eventually used when we are not being run in the Flask debugger.
media_dir = "/srv/osmo"


def event_stream():
    """
    Generate data to populate the client SSE stream.
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
    Provides the slide SSE stream.
    """

    return flask.Response(
        event_stream(),
        mimetype="text/event-stream"
    )


@app.route("/", methods=["GET"])
def home():
    """
    Provides the framework to display images based on the SSE stream.
    """

    return flask.render_template("client.html")


@app.route("/media/<path:name>", methods=["GET"])
def media(name):
    """
    Get a file from the media directory.
    """

    return flask.send_from_directory(media_dir, name)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mediadir",
        nargs="?",
        default="/srv/osmo",
        help="The directory to serve media files from"
    )
    args = parser.parse_args()

    r = redis.Redis(port=28692)
    media_dir = args.mediadir

    app.run(port=8000, debug=True)
