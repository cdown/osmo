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
    return flask.Response(event_stream(), mimetype="text/event-stream")

@app.route("/", methods=[ "GET" ])
def home():
    return """
<!doctype html>
<style type="text/css">
    body {
        background-attachment: fixed;
        background-position: 50% 50%;
        background-repeat: no-repeat no-repeat;
    }

    .constrainHeight {
        background-size: auto 100%;
    }

    .constrainWidth {
        background-size: 100% auto;
    }
</style>
<script type="text/javascript" src="http://code.jquery.com/jquery-2.0.0.min.js"></script>
<script>
    function scale_bg(url) {
        var img = new Image;
        img.src = url;
        var imageAspectRatio = img.width / img.height;
        var backgroundAspectRatio = $(window).width() / $(window).height();

        if (imageAspectRatio < backgroundAspectRatio) {
            $("body")
                .removeClass()
                .addClass('constrainHeight');
        } else {
            $("body")
                .removeClass()
                .addClass('constrainWidth');
        }
    }
    function sse() {
        var stream = new EventSource("/stream");
        stream.onmessage = function(e) {
            $("body").css("background-image",
                "url(/media/" + e.data + ")"
            );
            scale_bg("/media/" + e.data);
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
