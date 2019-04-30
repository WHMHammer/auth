import flask
from simplejson import dumps

import auth


@auth.cors("/reset_password")
def reset_password():
    form = flask.request.get_json()
    try:
        username = str(form["username"])
        email = str(form["email"]).lower()
        response = str(form["response"])
        salt = str(form["salt"])
        password_hash = str(form["password_hash"])
    except (KeyError, TypeError):
        return "{}", 400, {"Content-Type": "application/json"}

    if not(
        auth.check_username(username) and
        auth.check_email(email) and
        auth.check_salt(response) and
        auth.check_salt(salt) and
        auth.check_response(password_hash)
    ):
        return "{}", 400, {"Content-Type": "application/json"}

    conn = auth.connectDB()
    cur = conn.cursor()

    cur.execute(
        "select * from users where username=%s and email=%s and session=%s and status=%s limit 1;",
        (username, email, response, "verified")
    )
    if cur.fetchone() is not None:
        cur.execute(
            "update users set salt=%s,password_hash=%s where username=%s;",
            (salt, password_hash, username)
        )
        conn.commit()

        auth.send_email(
            auth.NOREPLY,
            email,
            "You have successfully changed your password!",
            "<p>Hello, dear %s:</p><p>You have successfully changed your password!</p><br/><p>Best regards,</p><p>%s</p>" % (
                username, auth.PROJECTNAME
            )
        )

    conn.close()

    return dumps({"user_token": auth.generate_user_token(username)})
