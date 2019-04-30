import flask

import auth


@auth.cors("/logout")
def logout():
    user_id = auth.check_user_token()

    if user_id:
        conn = auth.connectDB()
        cur = conn.cursor()

        cur.execute(
            "update users set session=%s where id=%s;",
            (auth.generate_salt(), user_id)
        )

        conn.commit()
        conn.close()

    return "{}"
