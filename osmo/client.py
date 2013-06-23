#!/usr/bin/env python

import sys
import flask
import redis

app = flask.Flask(__name__)

def event_stream():
    r = redis.Redis()
    ps = r.pubsub()
    ps.subscribe("osmo")
    for message in ps.listen():
        yield "data: %s\n\n" % message["data"]

@app.route("/stream", methods=[ "GET" ])
def stream():
    return flask.Response(event_stream(), mimetype="text/event-stream")

@app.route("/", methods=[ "GET" ])
def home():
    return """
<!doctype html>
<pre id="out"></pre>
<script>
    function sse() {
        var source = new EventSource('/stream');
        var out = document.getElementById('out');
        source.onmessage = function(e) {
            out.innerHTML = e.data + '\\n' + out.innerHTML;
        };
    }
    sse();
</script>
"""

@app.route("/media/<path:name>", methods=[ "GET" ])
def media(name):
    return flask.send_from_directory(media_dir, name)

if __name__ == "__main__":
    # TODO: Get media dir from config file
    media_dir = sys.argv[1]
    app.run(port=8000, debug=True)
