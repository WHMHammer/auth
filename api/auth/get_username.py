import flask

import auth


@auth.cors("/get_username")
def get_username():
    form = flask.request.get_json()
    try:
        email = str(form["email"]).lower()
    except (KeyError, TypeError):
        return "{}", 400, {"Content-Type": "application/json"}

    if not(
        auth.check_email(email)
    ):
        return "{}", 400, {"Content-Type": "application/json"}

    conn = auth.connectDB()
    cur = conn.cursor()

    cur.execute(
        "select username from users where email=%s and status=%s limit 1;",
        (email, "verified")
    )
    try:
        username = cur.fetchone()[0]
    except TypeError:
        pass
    else:
        auth.send_email(
            auth.NOREPLY,
            email,
            "Your username at %s" % auth.PROJECTNAME,
            "<p>Your username at %s is:</p><p>%s</p><br/><p>Best regards,</p><p>%s</p>" % (
                auth.PROJECTNAME,
                username,
                auth.PROJECTNAME
            )
        )

    conn.close()

    return "{}"
