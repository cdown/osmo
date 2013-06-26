#!/usr/bin/env python

import sys
import flask
import redis

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
    # TODO: Get media dir from config file
    media_dir = sys.argv[1]
    app.run(port=8000, debug=True)
