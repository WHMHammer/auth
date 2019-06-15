import flask

bp = flask.Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/", methods=("GET",))
def auth():
    return flask.redirect(flask.url_for(".login"))


@bp.route("/register", methods=("GET",))
def register():
    return flask.render_template(
        "auth/form.html",
        title="Register",
        button="register",
        scripts=(
            "lib/jsSHA/sha.js",
            "auth/register.js"
        ),
    )


@bp.route("/verify", methods=("GET",))
def verify():
    return flask.render_template(
        "auth/form.html",
        title="Verify",
        button="verify",
        scripts=(
            "lib/jsSHA/sha.js",
            "auth/verify.js"
        )
    )


@bp.route("/login", methods=("GET",))
def login():
    return flask.render_template(
        "auth/form.html",
        title="Login",
        button="login",
        scripts=(
            "lib/jsSHA/sha.js",
            "auth/login.js"
        )
    )


@bp.route("/get_username", methods=("GET",))
def get_username():
    return flask.render_template(
        "auth/form.html",
        title="Get username",
        button="get",
        scripts=("auth/get_username.js",)
    )


@bp.route("/request_password", methods=("GET",))
def request_password():
    return flask.render_template(
        "auth/form.html",
        title="Request password reset",
        button="request",
        scripts=("auth/request_password.js",)
    )


@bp.route("/reset_password", methods=("GET",))
def reset_password():
    return flask.render_template(
        "auth/form.html",
        title="Reset password",
        button="reset",
        scripts=("auth/reset_password.js",)
    )


@bp.route("/logout", methods=("GET",))
def logout():
    return flask.render_template("auth/logout.html")


@bp.route("/profile", methods=("GET",))
def profile():
    return flask.render_template("auth/profile.html")


@bp.route("/edit_profile", methods=("GET",))
def edit_profile():
    return flask.render_template("auth/edit_profile.html")
