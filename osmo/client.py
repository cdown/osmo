#!/usr/bin/env python

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

if __name__ == "__main__":
    app.run(port=8000, debug=True)
