import flask

import auth


@auth.bp.route("/profile", methods=("GET",))
def profile():
    return flask.render_template("profile.html")
