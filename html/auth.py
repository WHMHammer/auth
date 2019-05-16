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
            "auth/js/jsSHA/sha.js",
            "auth/js/register.js"
        ),
    )


@bp.route("/verify", methods=("GET",))
def verify():
    return flask.render_template(
        "auth/form.html",
        title="Verify",
        button="verify",
        scripts=(
            "auth/js/jsSHA/sha.js",
            "auth/js/verify.js"
        )
    )


@bp.route("/login", methods=("GET",))
def login():
    return flask.render_template(
        "auth/form.html",
        title="Login",
        button="login",
        scripts=(
            "auth/js/jsSHA/sha.js",
            "auth/js/login.js"
        )
    )


@bp.route("/get_username", methods=("GET",))
def get_username():
    return flask.render_template(
        "auth/form.html",
        title="Get username",
        button="get",
        scripts=("auth/js/get_username.js",)
    )


@bp.route("/request_password", methods=("GET",))
def request_password():
    return flask.render_template(
        "auth/form.html",
        title="Request password reset",
        button="request",
        scripts=("auth/js/request_password.js",)
    )


@bp.route("/reset_password", methods=("GET",))
def reset_password():
    return flask.render_template(
        "auth/form.html",
        title="Reset password",
        button="reset",
        scripts=("auth/js/reset_password.js",)
    )


@bp.route("/logout", methods=("GET",))
def logout():
    return flask.render_template("auth/logout.html")


@bp.route("/profile", methods=("GET",))
def profile():
    return flask.render_template("auth/profile.html")
