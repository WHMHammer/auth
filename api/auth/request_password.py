import flask

import auth


@auth.cors("/request_password")
def request_password():
    form = flask.request.get_json()
    try:
        email = str(form["email"]).lower()
    except (KeyError, TypeError):
        return "{}", 400, {"Content-Type": "application/json"}

    if not auth.check_email(email):
        return "{}", 400, {"Content-Type": "application/json"}

    conn = auth.connectDB()
    cur = conn.cursor()

    cur.execute(
        "select username,session from users where email=%s and status=%s limit 1;",
        (email, "verified")
    )
    try:
        username, session = cur.fetchone()
    except TypeError:
        pass
    else:
        reset_password_url = "https://%s/auth/reset_password" % auth.DOMAIN
        auth.send_email(
            auth.NOREPLY,
            email,
            "Reset your password at %s" % auth.PROJECTNAME,
            "<p>Hello, dear %s:</p><p>Your verification code is:</p><p><code>%s</code></p>Please click <a href=\"%s\">here</a> or paste the following url to your web browser to continue reseting your password:</p><p>%s</p><br/><p>Best regards,</p><p>%s</p>" % (
                username, session, reset_password_url, reset_password_url, auth.PROJECTNAME)
            )

    conn.close()

    return "{}"
