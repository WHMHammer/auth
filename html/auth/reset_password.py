import flask

import auth


@auth.bp.route("/reset_password", methods=("GET",))
def reset_password():
    return flask.render_template(
        "auth.html",
        title="Reset password",
        action_name="reset",
        ctrl_script_src="reset_password.js"
    )
