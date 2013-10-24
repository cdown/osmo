#!/usr/bin/env python

"""
Admin interface to osmo.

Usage: admin.py [options]

Options:
  --media-dir DIR  The directory to get media files from. [default: /srv/osmo]
  --port PORT      The port to run on. [default: 8001]
  --no-debug       Disable Flask debugging.
"""

import db
import errno
import flask
import os
import sys
import time
import werkzeug.utils
from config import config


app = flask.Flask(__name__)
app.secret_key = os.urandom(32)
d = db.Database()

def _static_dir(path):
    """
    Return a path within the static files directory.

    :param path: the path to append
    :returns: the path, prepended with the path to the static files directory
    :rtype: str
    """

    return os.path.join(os.path.dirname(__file__), "templates/static/" + path)


def _dtpicker_strptime(dtpicker_time):
    """
    Convert a dtpicker generated time into an epoch.

    :param dtpicker_time: the time format as generated by dtpicker
    :type dtpicker_time: str
    :returns: the associated epoch
    :rtype: int
    """

    time_struct = time.strptime(dtpicker_time, "%Y-%m-%d %H:%M")
    return time.mktime(time_struct)


@app.route("/", methods=["GET"])
def list_all():
    """
    List all slides.

    :returns: the admin interface index
    :rtype: :class:`flask.Response`
    """

    return flask.render_template(
        "admin/index.html",
        slides=d.slides_in_state("all", sort="start"),
        active_slides=d.slides_in_state("active"),
        error=flask.request.args.get("error", 0),
    )


@app.route("/rem/<path:slide_name>", methods=["GET"])
def rem(slide_name):
    """
    Remove a slide.

    :param slide_name: the slide name to remove
    :returns: a redirect to the admin interface index
    :rtype: :class:`flask.Response`
    """

    name = werkzeug.utils.secure_filename(name)
    try:
        os.remove(os.path.join(media_dir, name))
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e
        else:
            flask.flash("""Slide "%s" does not exist!""" % name)
            return flask.redirect(flask.url_for("list_all") + "?error=1")
    d.remove(name)
    flask.flash("""Okay, deleted slide "%s".""" % name)
    return flask.redirect(flask.url_for("list_all"))


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    Add a slide.

    :returns: if a POST, a redirect to the admin interface index, if a GET, the
        interface to add a slide
    :rtype: :class:`flask.Response`
    """

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
        flask.flash("""Okay, created slide "%s".""" % name)
        return flask.redirect(flask.url_for("list_all"))
    return flask.render_template("admin/add.html")


@app.route('/static/js/<path:filename>')
def static_js(filename):
    """
    Return a file relative to the static Javascript directory.

    :returns: a file relative to the static directory
    :rtype: :class:`flask.Response`
    """

    return flask.send_from_directory(_static_dir("js"), filename)


@app.route('/static/css/<path:filename>')
def static_css(filename):
    """
    Return a path to a file relative to the static CSS directory.

    :returns: a file relative to the static directory
    :rtype: :class:`flask.Response`
    """

    return flask.send_from_directory(_static_dir("css"), filename)


@app.route('/static/img/<path:filename>')
def static_img(filename):
    """
    Return a path to a file relative to the static image directory.

    :returns: a file relative to the static directory
    :rtype: :class:`flask.Response`
    """

    return flask.send_from_directory(_static_dir("img"), filename)


if __name__ == "__main__":
    app.run(port=config["admin"]["port"])
