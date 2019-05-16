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
        return "{}", 400

    if not(
        auth.check_username(username) and
        auth.check_salt(salt) and
        auth.check_response(password_hash) and
        auth.check_email(email)
    ):
        return "{}", 400

    conn = auth.connectDB()
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

    challenge = auth.generate_salt()

    cur.execute("""
        DELETE FROM users
        WHERE username = %s OR email = %s;
    """, (username, email))

    cur.execute("""
        INSERT INTO users(username, email, salt, password_hash, challenge)
        VALUES(%s, %s, %s, %s, %s);
    """, (username, email, salt, password_hash, challenge))

    try:
        verify_url = "http://%s/auth/verify.html" % (auth.DOMAIN)
        auth.send_email(
            auth.NOREPLY,
            email,
            "Verify your registration at %s" % auth.PROJECTNAME,
            """
                <p>Hello, dear %s:</p>
                <p>Your verification code is:</p>
                <p><code>%s</code></p>
                <p>Please click <a href="%s">here</a> or paste the following url to your web browser to verify your registration:</p>
                <p>%s</p>
                <br/>
                <p>Best regards,</p>
                <p>%s</p>
            """ % (username, challenge+salt, verify_url, verify_url, auth.PROJECTNAME)
        )
    except auth.smtplib.SMTPRecipientsRefused:
        conn.close()
        return dumps({
            "err_msg": ["The email address you entered is invalid."]}
        ), 403

    conn.commit()
    conn.close()

    return "{}"
