import flask
from simplejson import dumps
from time import time

import auth


@auth.cors("/verify")
def verify():
    form = flask.request.get_json()
    try:
        username = str(form["username"])
        response = str(form["response"])
        email = str(form["email"]).lower()
    except (KeyError, TypeError):
        return "{}", 400

    if not(
        auth.check_username(username) and
        auth.check_response(response) and
        auth.check_email(email)
    ):
        return "{}", 400

    conn = auth.connectDB()
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

    if response != auth.hash_r(challenge, password_hash):
        conn.close()
        return "{}", 403

    cur.execute("""
        UPDATE users
        SET status = %s, challenge = %s
        WHERE username = %s;
    """, ("verified", auth.generate_salt(), username))

    conn.commit()
    conn.close()

    auth.send_email(
        auth.NOREPLY,
        email,
        "Your registration at %s is verified" % auth.PROJECTNAME,
        """
            <p>Dear %s:</p>
            <p>Your registration at %s is verified. Have fun!</p>
            <br/>
            <p>Best rgards,</p>
            <p>%s</p>
        """ % (username, auth.PROJECTNAME, auth.PROJECTNAME)
    )

    return dumps({
        "user_token": auth.generate_user_token(username)
    })
