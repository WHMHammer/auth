import flask
from simplejson import dumps

import auth


@auth.bp.route("/register", methods=("GET",))
def register():
    return flask.render_template(
        "auth.html",
        title="Register",
        action_name="register",
        ctrl_script_src="register.js"
    )
