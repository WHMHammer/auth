import flask
from time import time

import auth


@auth.bp.route("/login", methods=("GET",))
def login():
    return flask.render_template(
        "auth.html",
        title="Login",
        action_name="login",
        ctrl_script_src="login.js"
    )
