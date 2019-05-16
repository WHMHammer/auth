import flask

import auth


@auth.cors("/request_password")
def request_password():
    form = flask.request.get_json()
    try:
        email = str(form["email"]).lower()
    except (KeyError, TypeError):
        return "{}", 400

    if not auth.check_email(email):
        return "{}", 400

    conn = auth.connectDB()
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

    challenge = auth.rand_str(32)

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

    reset_password_url = "http://%s/auth/reset_password" % auth.DOMAIN
    auth.send_email(
        auth.NOREPLY,
        email,
        "Reset your password at %s" % auth.PROJECTNAME,
        """
            <p>Hello, dear %s:</p>
            <p>Your verification code is:</p>
            <p><code>%s</code></p>
            <p>Please click <a href="%s">here</a> or paste the following url to your web browser to reset your password:</p>
            <p>%s</p>
            <br/>
            <p>Best regards,</p>
            <p>%s</p>
        """ % (username, challenge, reset_password_url, reset_password_url, auth.PROJECTNAME))

    conn.close()

    return "{}"
