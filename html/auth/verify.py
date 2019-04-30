import flask
from time import time

import auth


@auth.bp.route("/verify", methods=("GET",))
def verify():
    return flask.render_template(
        "auth.html",
        title="Verify",
        action_name="verify",
        ctrl_script_src="verify.js"
    )
