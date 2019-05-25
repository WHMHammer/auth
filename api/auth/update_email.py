import flask
from simplejson import dumps

import auth


@auth.cors("/update_email")
def update_email():
    user = auth.check_user_token()

    if user is None:
        return "{}", 403

    try:
        email = str(flask.request.get_json()["email"])
    except KeyError:
        return "{}", 400

    if not auth.check_email(email):
        return '{}', 400

    conn = auth.connectDB()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE users
            SET email = %s
            WHERE id = %s;
        """, (email, user["id"]))
    except auth.sql.IntegrityError:
        conn.close()
        return dumps({
            "err_msg": ["The email address you entered has already been used."]
        }), 403

    try:
        auth.send_email(
            auth.NOREPLY,
            user["email"],
            "You have just changed your email address at %s" % auth.PROJECTNAME,
            """
                <p>Hello, dear %s</p>
                <p>You have just changed your email address to <strong>%s</strong>. If you did not perform this action, please update your password immediately to protect your account.</p>
                <br/>
                <p>Best regards,</p>
                <p>%s</p>
            """ % (user["username"], email, auth.PROJECTNAME)
        )
    except auth.smtplib.SMTPRecipientsRefused:
        conn.close()
        return dumps({
            "err_msg": ["The email address you entered is invalid."]}
        ), 403

    conn.commit()
    conn.close()

    return "{}"
