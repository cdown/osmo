#!/usr/bin/env python

"""Client and web interface for osmo."""

import sys
import flask
import redis
import argparse

app = flask.Flask(__name__)
r = redis.Redis()

# This is only eventually used when we are not being run in the Flask debugger.
media_dir = "/srv/osmo"

def event_stream():
    ps = r.pubsub()
    ps.subscribe("osmo")
    for message in ps.listen():
        try:
            data = message["data"].decode("utf8")
        except AttributeError:
            data = message["data"]

        yield "data: %s\n\n" % data

@app.route("/stream", methods=[ "GET" ])
def stream():
    return flask.Response(
        event_stream(),
        mimetype="text/event-stream"
    )

@app.route("/", methods=[ "GET" ])
def home():
    return flask.render_template("client.html")

@app.route("/media/<path:name>", methods=[ "GET" ])
def media(name):
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
    parser.add_argument(
        "--test",
        action="store_true",
        help="Whether to use the testing database"
    )
    args = parser.parse_args()

    r = redis.Redis(db=int(args.test))
    media_dir = args.mediadir

    app.run(port=8000, debug=True)
