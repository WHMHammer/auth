import flask
from simplejson import dumps

import auth


@auth.cors("/update_username")
def update_username():
    user = auth.check_user_token()

    if user is None:
        return "{}", 403

    try:
        username = str(flask.request.get_json()["username"])
    except KeyError:
        return "{}", 400

    if not auth.check_username(username):
        return '{}', 400

    conn = auth.connectDB()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE users
            SET username = %s
            WHERE id = %s;
        """, (username, user["id"]))
    except auth.sql.IntegrityError:
        conn.close()
        return dumps({
            "err_msg": ["The email address you entered has already been used."]
        }), 403

    conn.commit()
    conn.close()

    auth.send_email(
        auth.NOREPLY,
        user["email"],
        "You have just changed your username at %s" % auth.PROJECTNAME,
        """
            <p>Hello, dear %s</p>
            <p>You have just changed your username to <strong>%s</strong>. If you did not perform this action, please update your password immediately to protect your account.</p>
            <br/>
            <p>Best regards,</p>
            <p>%s</p>
        """ % (user["username"], username, auth.PROJECTNAME)
    )

    return "{}"
