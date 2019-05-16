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
        return "{}", 400

    if not(
        auth.check_username(username) and
        auth.check_email(email) and
        len(response) == 32 and
        auth.check_salt(salt) and
        auth.check_response(password_hash)
    ):
        return "{}", 400

    conn = auth.connectDB()
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

    auth.send_email(
        auth.NOREPLY,
        email,
        "You have successfully changed your password!",
        """
            <p>Hello, dear %s:</p>
            <p>You have successfully changed your password!</p>
            <br/>
            <p>Best regards,</p>
            <p>%s</p>
        """ % (username, auth.PROJECTNAME)
    )

    return dumps({
        "user_token": auth.generate_user_token(username)
    })
