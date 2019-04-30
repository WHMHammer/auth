import flask
from simplejson import dumps

import auth


@auth.cors("/register")
def register():
    form = flask.request.get_json()
    try:
        username = str(form["username"])
        salt = str(form["salt"])
        password_hash = str(form["password_hash"])
        email = str(form["email"]).lower()
    except (KeyError, TypeError):
        return "{}", 400, {"Content-Type": "application/json"}

    if not(
        auth.check_username(username) and
        auth.check_salt(salt) and
        auth.check_response(password_hash) and
        auth.check_email(email)
    ):
        return "{}", 400, {"Content-Type": "application/json"}

    conn = auth.connectDB()
    cur = conn.cursor()

    err = False
    err_msg = list()

    cur.execute(
        "select * from users where email=%s and status!=%s limit 1;",
        (email, "unverified")
    )
    if cur.fetchone() is not None:
        err = True
        err_msg.append("The email address you entered has already been used.")

    cur.execute(
        "select * from users where username=%s and status!=%s limit 1;",
        (username, "unverified")
    )
    if cur.fetchone() is not None:
        err = True
        err_msg.append("The username you entered has already been used.")

    if err:
        conn.close()
        return dumps({"err_msg": err_msg}), 403, {"Content-Type": "application/json"}

    session = auth.generate_salt()

    cur.execute(
        "delete from users where username=%s or email=%s;",
        (username, email)
    )
    cur.execute(
        "insert into users(username,salt,password_hash,email,session,challenge) values(%s,%s,%s,%s,%s,%s);",
        (username, salt, password_hash, email, session, auth.generate_salt())
    )

    try:
        verify_url = "https://%s/auth/verify.html" % (auth.DOMAIN)
        auth.send_email(
            auth.NOREPLY,
            email,
            "Verify your registration at %s" % auth.PROJECTNAME,
            "<p>Hello, dear %s:</p><p>Your verification code is:</p><p><code>%s</code></p>Please click <a href=\"%s\">here</a> or paste the following url to your web browser to verify your registration:</p><p>%s</p><br/><p>Best regards,</p><p>%s</p>" % (
                username, session+salt, verify_url, verify_url, auth.PROJECTNAME
            )
        )
    except auth.smtplib.SMTPRecipientsRefused:
        conn.close()
        return dumps({
            "err_msg": ["The email address you entered is invalid."]
        }), 403, {"Content-Type": "application/json"}

    conn.commit()
    conn.close()

    return "{}"
