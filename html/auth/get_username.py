import flask

import auth


@auth.bp.route("/get_username", methods=("GET",))
def get_username():
    return flask.render_template(
        "auth.html",
        title="Forgot username",
        action_name="submit",
        ctrl_script_src="get_username.js"
    )
