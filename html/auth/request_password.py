import flask

import auth


@auth.bp.route("/request_password", methods=("GET",))
def request_password():
    return flask.render_template(
        "auth.html",
        title="Request password",
        action_name="request",
        ctrl_script_src="request_password.js"
    )
