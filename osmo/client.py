#!/usr/bin/env python

"""Client and web interface for osmo."""

import sys
import flask
import redis
import argparse

app = flask.Flask(__name__)
r = redis.Redis()

def event_stream():
    ps = r.pubsub()
    ps.subscribe("osmo")
    for message in ps.listen():
        yield "data: %s\n\n" % message["data"]

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
    args = parser.parse_args()

    media_dir = args.mediadir
    app.run(port=8000, debug=True)
