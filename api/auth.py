from simplejson import dumps
from time import time
from urllib.parse import unquote

from lib import *
from lib.auth import *

bp = flask.Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("POST",))
def register():
    try:
        username = str(flask.g.form["username"])
        salt = str(flask.g.form["salt"])
        password_hash = str(flask.g.form["password_hash"])
        email = str(flask.g.form["email"]).lower()
    except (KeyError, TypeError):
        return "{}", 400

    if not(
        check_username(username) and
        check_salt(salt) and
        check_response(password_hash) and
        check_email(email)
    ):
        return "{}", 400

    cur = flask.g.db.cursor()

    err = False
    err_msg = list()

    cur.execute("""
        SELECT *
        FROM users
        WHERE email = %s AND status != %s
        LIMIT 1;
    """, (email, "unverified"))

    if cur.fetchone() is not None:
        err = True
        err_msg.append("The email address you entered has already been used.")

    cur.execute("""
        SELECT *
        FROM users
        WHERE username = %s AND status != %s
        LIMIT 1;
    """, (username, "unverified"))

    if cur.fetchone() is not None:
        err = True
        err_msg.append("The username you entered has already been used.")

    if err:
        return dumps({"err_msg": err_msg}), 403

    challenge = generate_salt()

    cur.execute("""
        DELETE FROM users
        WHERE username = %s OR email = %s;
    """, (username, email))

    cur.execute("""
        INSERT INTO users(username, email, salt, password_hash, challenge)
        VALUES(%s, %s, %s, %s, %s);
    """, (username, email, salt, password_hash, challenge))

    try:
        verify_url = "%s/auth/verify" % (domain)
        send_email(
            noreply,
            email,
            "Verify your registration at %s" % project_name,
            """
                <p>Hello, dear %s:</p>
                <p>Your verification code is:</p>
                <p><code>%s</code></p>
                <p>Please click <a href="%s">here</a> or paste the following url to your web browser to verify your registration:</p>
                <p>%s</p>
                <br/>
                <p>Best regards,</p>
                <p>%s</p>
            """ % (username, challenge+salt, verify_url, verify_url, project_name)
        )
    except smtplib.SMTPRecipientsRefused:
        return dumps({
            "err_msg": ["The email address you entered is invalid."]}
        ), 403

    flask.g.db.commit()

    return "{}"


@bp.route("/register", methods=("PUT",))
def verify():
    try:
        username = str(flask.g.form["username"])
        response = str(flask.g.form["response"])
        email = str(flask.g.form["email"]).lower()
    except (KeyError, TypeError):
        return "{}", 400

    if not(
        check_username(username) and
        check_response(response) and
        check_email(email)
    ):
        return "{}", 400

    cur = flask.g.db.cursor()

    cur.execute("""
        SELECT password_hash, challenge
        FROM users
        WHERE username = %s AND email = %s AND status = %s
        LIMIT 1;
    """, (username, email, "unverified"))

    try:
        password_hash, challenge = cur.fetchone()
    except TypeError:
        return "{}", 403

    if response != hash(challenge, password_hash):
        return "{}", 403

    cur.execute("""
        UPDATE users
        SET status = %s, challenge = %s
        WHERE username = %s;
    """, ("verified", generate_salt(), username))

    send_email(
        noreply,
        email,
        "Your registration at %s is verified" % project_name,
        """
            <p>Dear %s:</p>
            <p>Your registration at %s is verified. Have fun!</p>
            <br/>
            <p>Best rgards,</p>
            <p>%s</p>
        """ % (username, project_name, project_name)
    )

    flask.g.db.commit()

    return dumps({
        "user_token": generate_user_token(username)
    })


@bp.route("/login", methods=("GET",))
def get_challenge():
    try:
        username = unquote(str(flask.g.form["username"]))
    except (KeyError, TypeError):
        return "{}", 400

    if not(
        check_username(username)
    ):
        return "{}", 400

    cur = flask.g.db.cursor()

    cur.execute("""
        SELECT salt
        FROM users
        WHERE username = %s AND status = %s
        LIMIT 1;
    """, (username, "verified"))

    try:
        salt = cur.fetchone()[0]
    except TypeError:
        
        return "{}", 404

    challenge = generate_salt()

    cur.execute("""
        UPDATE users
        SET challenge = %s
        WHERE username = %s;
    """, (challenge, username))

    flask.g.db.commit()

    return dumps({
        "salt": salt,
        "challenge": challenge
    })


@bp.route("/login", methods=("POST",))
def login():
    try:
        username = str(flask.g.form["username"])
        response = str(flask.g.form["response"])
    except (KeyError, TypeError):
        return "{}", 400

    if not(
        check_username(username) and
        check_response(response)
    ):
        return "{}", 400

    cur = flask.g.db.cursor()

    cur.execute("""
        SELECT password_hash, challenge
        FROM users
        WHERE username = %s AND status = %s
        LIMIT 1;
    """, (username, "verified"))
    try:
        password_hash, challenge = cur.fetchone()
    except TypeError:
        return "{}", 403

    if response != hash(challenge, password_hash):
        return "{}", 403

    cur.execute("""
        UPDATE users
        SET challenge = %s
        WHERE username = %s;
    """, (generate_salt(), username))

    flask.g.db.commit()

    return dumps({
        "user_token": generate_user_token(username)
    })


@bp.route("/login", methods=("DELETE",))
def logout():
    user = get_user_token(flask.g.form.get("user_token", None))

    if user is None:
        return "{}"

    cur = flask.g.db.cursor()

    cur.execute("""
        DELETE FROM sessions
        WHERE user_id = %s AND session = %s;
    """, (user["id"], flask.request.get_json().get("user_token")["session"]))

    flask.g.db.commit()

    return "{}"


@bp.route("/password", methods=("GET",))
def request_password_reset():
    try:
        email = unquote(str(flask.g.form["email"]))
    except (KeyError, TypeError):
        return "{}", 400

    if not check_email(email):
        return "{}", 400

    cur = flask.g.db.cursor()

    cur.execute("""
        SELECT id, username
        FROM users
        WHERE email = %s AND status=%s
        LIMIT 1;
    """, (email, "verified"))

    try:
        user_id, username = cur.fetchone()
    except TypeError:
        return "{}"

    challenge = rand_str(32)

    cur.execute("""
        UPDATE users
        SET status = %s
        WHERE id = %s;
    """, (challenge, user_id))

    cur.execute("""
        DELETE FROM sessions
        WHERE user_id = %s;
    """, (user_id,))

    flask.g.db.commit()

    reset_password_url = "%s/auth/reset_password" % domain
    send_email(
        noreply,
        email,
        "Reset your password at %s" % project_name,
        """
            <p>Hello, dear %s:</p>
            <p>Your verification code is:</p>
            <p><code>%s</code></p>
            <p>Please click <a href="%s">here</a> or paste the following url to your web browser to reset your password:</p>
            <p>%s</p>
            <br/>
            <p>Best regards,</p>
            <p>%s</p>
        """ % (username, challenge, reset_password_url, reset_password_url, project_name))

    return "{}"


@bp.route("/password", methods=("PUT",))
def reset_password():
    try:
        username = str(flask.g.form["username"])
        email = str(flask.g.form["email"]).lower()
        response = str(flask.g.form["response"])
        salt = str(flask.g.form["salt"])
        password_hash = str(flask.g.form["password_hash"])
    except (KeyError, TypeError):
        return "{}", 400

    if not(
        check_username(username) and
        check_email(email) and
        len(response) == 32 and
        check_salt(salt) and
        check_response(password_hash)
    ):
        return "{}", 400

    cur = flask.g.db.cursor()

    cur.execute("""
        SELECT *
        FROM users
        WHERE username = %s AND email = %s AND status = %s
        LIMIT 1;
    """, (username, email, response))

    if cur.fetchone() is None:
        return "{}", 403

    cur.execute("""
        UPDATE users
        SET status = %s, salt = %s, password_hash = %s
        WHERE username=%s;
    """, ("verified", salt, password_hash, username))

    flask.g.db.commit()

    send_email(
        noreply,
        email,
        "You have successfully changed your password!",
        """
            <p>Hello, dear %s:</p>
            <p>You have successfully changed your password!</p>
            <br/>
            <p>Best regards,</p>
            <p>%s</p>
        """ % (username, project_name)
    )

    return dumps({
        "user_token": generate_user_token(username)
    })


@bp.route("/user", methods=("GET",))
def get_username():
    try:
        email = unquote(str(flask.g.form["email"]))
    except (KeyError, TypeError):
        return "{}", 400

    if not(
        check_email(email)
    ):
        return "{}", 400

    cur = flask.g.db.cursor()

    cur.execute("""
        SELECT username
        FROM users
        WHERE email = %s AND status = %s
        LIMIT 1;
    """, (email, "verified"))

    try:
        username = cur.fetchone()[0]
    except TypeError:
        pass
    else:
        send_email(
            noreply,
            email,
            "Your username at %s" % project_name,
            """
                <p>Your username at %s is:</p>
                <p>%s</p>
                <br/>
                <p>Best regards,</p>
                <p>%s</p>
            """ % (project_name, username, project_name)
        )

    return "{}"


@bp.route("/user", methods=("PUT",))
def update_user_info():
    user = get_user_token(flask.g.form.get("user_token", None))

    if user is None:
        return "{}", 401

    cur = flask.g.db.cursor()

    if "username" in form:
        username = str(flask.g.form["username"])
        if not check_username(username):
            return "{}", 400

        conn.execute("""
            UPDATE users
            SET username = %s
            WHERE id = %s;
        """, (username, user["user_id"]))

    if "email" in form:
        email = str(flask.g.form["email"])
        if not check_email(email):
            return "{}", 400

        conn.execute("""
            UPDATE users
            SET email = %s
            WHERE id = %s;
        """, (email, user["user_id"]))

    if "avatar" in form:
        avatar = str(flask.g.form["avatar"])
        if not check_url(avatar):
            return "{}", 400

        conn.execute("""
            UPDATE users
            SET avatar = %s
            WHERE id = %s;
        """, (avatar, user["user_id"]))

    if "password_hash" in form:
        try:
            salt = str(flask.g.form["salt"])
            password_hash = str(form["password_hash"])
        except (KeyError, TypeError):
            return "{}", 400

        if not(
            check_salt(salt) and
            check_response(password_hash)
        ):
            return "{}", 400

        conn.execute("""
            UPDATE users
            SET salt = %s, password_hash = %s
            WHERE id = %s;
        """, (salt, password_hash, user["user_id"]))

    flask.g.db.commit()

    return "{}"


@bp.route("/user", methods=("DELETE",))
def delete_user():
    user = get_user_token(flask.g.form.get("user_token", None))

    if user is None:
        return "{}"

    cur = flask.g.db.cursor()

    cur.execute("""
        DELETE FROM sessions
        WHERE user_id = %s;
    """, (user["user_id"],))

    cur.execute("""
        DELETE FROM users
        WHERE user_id = %s;
    """, (user["user_id"],))

    flask.g.db.commit()

    return "{}"
