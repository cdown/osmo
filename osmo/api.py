#!/usr/bin/env python

"""Read-only API for osmo."""

import argparse
import bottle
import db

@bottle.get("/current")
def items():
    return { "items": d.current() }

@bottle.get("/media/:name")
@bottle.validate(name=str)
def media(name):
    return bottle.static_file(name, root=media_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mediadir",
        help="Media directory.",
    )
    parser.add_argument(
        "--live",
        help="Use the live database instead of testing. (Dangerous!)",
        action="store_true"
    )
    args = parser.parse_args()
    is_test = not args.live
    media_dir = args.mediadir

    d = db.Database(test=is_test)
    bottle.run(host='0.0.0.0', port=8080, debug=is_test)
