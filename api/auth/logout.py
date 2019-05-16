import flask

import auth


@auth.cors("/logout")
def logout():
    user = auth.check_user_token()

    if user is None:
        return "{}"

    conn = auth.connectDB()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM sessions
        WHERE user_id = %s AND session = %s;
    """, (user["id"], flask.request.get_json().get("user_token")["session"]))

    conn.commit()
    conn.close()

    return "{}"
