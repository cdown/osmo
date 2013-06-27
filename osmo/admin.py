#!/usr/bin/env python

"""Admin interface for osmo."""

import argparse
import calendar
import db
import errno
import flask
import os
import sys
import time
import werkzeug.utils

app = flask.Flask(__name__)
app.secret_key = os.urandom(32)
d = db.Database()

# This is only eventually used when we are not being run in the Flask debugger.
media_dir = "/srv/osmo"

def _static_dir(path):
    return os.path.join(os.path.dirname(__file__), "templates/static/" + path)

def _dtpicker_strptime(data):
    stripped = time.strptime(data, "%Y-%m-%d %H:%M")
    return calendar.timegm(stripped)

@app.route("/", methods=[ "GET" ])
def list_all():
    return flask.render_template(
        "admin/index.html",
        items=d.get_all_metadata(),
        active_items=d.get_state(state="active"),
        error=flask.request.args.get("error", 0),
    )

@app.route("/rem/<path:name>", methods=[ "GET" ])
def rem(name):
    name = werkzeug.utils.secure_filename(name)
    try:
        os.remove(os.path.join(media_dir, name))
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e
        else:
            flask.flash("""Item "%s" does not exist!""" % name)
            return flask.redirect(flask.url_for("list_all") + "?error=1")
    d.rem(name)
    flask.flash("""Okay, deleted item "%s".""" % name)
    return flask.redirect(flask.url_for("list_all"))

@app.route("/add", methods=[ "GET", "POST" ])
def add():
    if flask.request.method == "POST":
        u_file = flask.request.files["file"]

        name = werkzeug.utils.secure_filename(u_file.filename)
        start = _dtpicker_strptime(flask.request.form["start"])
        end = _dtpicker_strptime(flask.request.form["end"])
        duration = int(flask.request.form["duration"])
        rank = int(flask.request.form["rank"])

        if not u_file:
            abort(400)

        u_file.save(os.path.join(media_dir, name))
        d.add(name, start, end, duration, rank)
        flask.flash("""Okay, created item "%s".""" % name)
        return flask.redirect(flask.url_for("list_all"))
    return flask.render_template(
        "admin/add.html",
    )

@app.route('/static/js/<path:filename>')
def static_js(filename):
    return flask.send_from_directory(_static_dir("js"), filename)

@app.route('/static/css/<path:filename>')
def static_css(filename):
    return flask.send_from_directory(_static_dir("css"), filename)

@app.route('/static/img/<path:filename>')
def static_img(filename):
    return flask.send_from_directory(_static_dir("img"), filename)

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
    app.run(port=8001, debug=True)
