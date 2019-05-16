import flask
from simplejson import dumps

import auth


@auth.cors("/get_challenge")
def get_challenge():
    form = flask.request.get_json()
    try:
        username = str(form["username"])
    except (KeyError, TypeError):
        return "{}", 400

    if not(
        auth.check_username(username)
    ):
        return "{}", 400

    conn = auth.connectDB()
    cur = conn.cursor()

    cur.execute("""
        SELECT salt
        FROM users
        WHERE username = %s AND status = %s
        LIMIT 1;
    """, (username, "verified"))

    try:
        salt = cur.fetchone()[0]
    except TypeError:
        conn.close()
        return "{}", 404

    challenge = auth.generate_salt()

    cur.execute("""
        UPDATE users
        SET challenge = %s
        WHERE username = %s;
    """, (challenge, username))

    conn.commit()
    conn.close()

    return dumps({
        "salt": salt,
        "challenge": challenge
    })
