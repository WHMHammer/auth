import flask
from simplejson import dumps

import auth


@auth.cors("/update_avatar")
def update_avatar():
    user = auth.check_user_token()

    if user is None:
        return "{}", 403

    try:
        avatar = str(flask.request.get_json()["avatar"])
    except KeyError:
        return "{}", 400

    if not auth.check_link(avatar):
        return '{}', 400

    conn = auth.connectDB()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET avatar = %s
        WHERE id = %s;
    """, (avatar, user["id"]))

    conn.commit()
    conn.close()

    return "{}"
