import flask
from simplejson import dumps

import auth


@auth.cors("/login")
def login():
    form = flask.request.get_json()
    try:
        username = str(form["username"])
        response = str(form["response"])
    except (KeyError, TypeError):
        return "{}", 400

    if not(
        auth.check_username(username) and
        auth.check_response(response)
    ):
        return "{}", 400

    conn = auth.connectDB()
    cur = conn.cursor()

    cur.execute("""
        SELECT password_hash, challenge
        FROM users
        WHERE username = %s AND status = %s
        LIMIT 1;
    """, (username, "verified"))
    try:
        password_hash, challenge = cur.fetchone()
    except TypeError:
        return "{}", 403

    if response != auth.hash_r(challenge, password_hash):
        conn.close()
        return "{}", 403

    cur.execute("""
        UPDATE users
        SET challenge = %s
        WHERE username = %s;
    """, (auth.generate_salt(), username))

    conn.commit()
    conn.close()

    return dumps({
        "user_token": auth.generate_user_token(username)
    })
