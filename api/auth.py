import flask
from simplejson import dumps
from time import time
from urllib.parse import unquote

from lib import *
from lib.auth import *

bp = flask.Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_request
def options():
    if flask.request.method == "OPTIONS":
        return "{}"


@bp.after_request
def header(rp):
    rp.headers.set("Access-Control-Allow-Origin", "*")
    rp.headers.set("Access-Control-Allow-Methods", "OPTIONS, GET, POST, PUT, DELETE")
    rp.headers.set("Access-Control-Allow-Headers", "Content-Type")
    rp.headers.set("Content-Type", "application/json")
    return rp


@bp.route("/register", methods=("POST",))
def register():
    form = flask.request.get_json()
    try:
        username = str(form["username"])
        salt = str(form["salt"])
        password_hash = str(form["password_hash"])
        email = str(form["email"]).lower()
    except (KeyError, TypeError):
        return "{}", 400

    if not(
        check_username(username) and
        check_salt(salt) and
        check_response(password_hash) and
        check_email(email)
    ):
        return "{}", 400

    conn = connect_db()
    cur = conn.cursor()

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
        conn.close()
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
        verify_url = "https://%s/auth/verify" % (domain)
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
        conn.close()
        return dumps({
            "err_msg": ["The email address you entered is invalid."]}
        ), 403

    conn.commit()
    conn.close()

    return "{}"


@bp.route("/register", methods=("PUT",))
def verify():
    form = flask.request.get_json()
    try:
        username = str(form["username"])
        response = str(form["response"])
        email = str(form["email"]).lower()
    except (KeyError, TypeError):
        return "{}", 400

    if not(
        check_username(username) and
        check_response(response) and
        check_email(email)
    ):
        return "{}", 400

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT password_hash, challenge
        FROM users
        WHERE username = %s AND email = %s AND status = %s
        LIMIT 1;
    """, (username, email, "unverified"))

    try:
        password_hash, challenge = cur.fetchone()
    except TypeError:
        conn.close()
        return "{}", 403

    if response != hash(challenge, password_hash):
        conn.close()
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

    conn.commit()
    conn.close()

    return dumps({
        "user_token": generate_user_token(username)
    })


@bp.route("/login", methods=("GET",))
def get_challenge():
    try:
        username = unquote(str(flask.request.args["username"]))
    except (KeyError, TypeError):
        return "{}", 400

    if not(
        check_username(username)
    ):
        return "{}", 400

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT salt
        FROM users
        WHERE username = %s AND status = %s
        LIMIT 1;
    """, (username, "verified"))

    try:
        salt = cur.fetchone()[0]
    except TypeError:
        conn.close()
        return "{}", 404

    challenge = generate_salt()

    cur.execute("""
        UPDATE users
        SET challenge = %s
        WHERE username = %s;
    """, (challenge, username))

    conn.commit()
    conn.close()

    return dumps({
        "salt": salt,
        "challenge": challenge
    })


@bp.route("/login", methods=("POST",))
def login():
    form = flask.request.get_json()
    try:
        username = str(form["username"])
        response = str(form["response"])
    except (KeyError, TypeError):
        return "{}", 400

    if not(
        check_username(username) and
        check_response(response)
    ):
        return "{}", 400

    conn = connect_db()
    cur = conn.cursor()

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
        conn.close()
        return "{}", 403

    cur.execute("""
        UPDATE users
        SET challenge = %s
        WHERE username = %s;
    """, (generate_salt(), username))

    conn.commit()
    conn.close()

    return dumps({
        "user_token": generate_user_token(username)
    })


@bp.route("/login", methods=("DELETE",))
def logout():
    user = check_user_token()

    if user is None:
        return "{}"

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM sessions
        WHERE user_id = %s AND session = %s;
    """, (user["id"], flask.request.get_json().get("user_token")["session"]))

    conn.commit()
    conn.close()

    return "{}"


@bp.route("/password", methods=("GET",))
def request_reset_password():
    try:
        email = unquote(str(flask.request.args["email"]))
    except (KeyError, TypeError):
        return "{}", 400

    if not check_email(email):
        return "{}", 400

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username
        FROM users
        WHERE email = %s AND status=%s
        LIMIT 1;
    """, (email, "verified"))

    try:
        user_id, username = cur.fetchone()
    except TypeError:
        conn.close()
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

    conn.commit()

    reset_password_url = "https://%s/auth/reset_password" % domain
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

    conn.close()

    return "{}"


@bp.route("/password", methods=("PUT",))
def reset_password():
    form = flask.request.get_json()
    try:
        username = str(form["username"])
        email = str(form["email"]).lower()
        response = str(form["response"])
        salt = str(form["salt"])
        password_hash = str(form["password_hash"])
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

    conn = connect_db()
    cur = conn.cursor()

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

    conn.commit()
    conn.close()

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
def get_user_info():
    return "{}", 501


@bp.route("/user", methods=("PUT",))
def update_user_info():
    user = check_user_token()

    if user is None:
        return "{}", 401

    form = flask.request.get_json()
    conn = connect_db()
    cur = conn.cursor()

    if "username" in form:
        username = str(form["username"])
        if not check_username(username):
            conn.close()
            return "{}", 400

        conn.execute("""
            UPDATE users
            SET username = %s
            WHERE id = %s;
        """, (username, user["user_id"]))

    if "email" in form:
        email = str(form["email"])
        if not check_email(email):
            conn.close()
            return "{}", 400

        conn.execute("""
            UPDATE users
            SET email = %s
            WHERE id = %s;
        """, (email, user["user_id"]))

    if "avatar" in form:
        avatar = str(form["avatar"])
        if not check_url(avatar):
            conn.close()
            return "{}", 400

        conn.execute("""
            UPDATE users
            SET avatar = %s
            WHERE id = %s;
        """, (avatar, user["user_id"]))

    if "password_hash" in form:
        try:
            salt = str(form["salt"])
            password_hash = str(form["password_hash"])
        except (KeyError, TypeError):
            conn.close()
            return "{}", 400

        if not(
            check_salt(salt) and
            check_response(password_hash)
        ):
            conn.close()
            return "{}", 400

        conn.execute("""
            UPDATE users
            SET salt = %s, password_hash = %s
            WHERE id = %s;
        """, (salt, password_hash, user["user_id"]))

    conn.commit()
    conn.close()

    return "{}"


@bp.route("/user", methods=("DELETE",))
def delete_user():
    user = check_user_token()

    if user is None:
        return "{}"

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM sessions
        WHERE user_id = %s;
    """, (user["user_id"],))

    cur.execute("""
        DELETE FROM users
        WHERE user_id = %s;
    """, (user["user_id"],))

    conn.commit()
    conn.close()

    return "{}"
