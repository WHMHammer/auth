import flask

import auth


@auth.bp.route("/profile",methods=("GET",))
def profile():
    if not auth.check_client_session():
        return flask.redirect("/")
    
    user_id=flask.session.get("user_id")

    conn=auth.connectDB()
    cur=conn.cursor()

    cur.execute("select username,email,avatar from users where id=%s limit 1;",(user_id,))
    username,email,avatar_src=cur.fetchone()

    conn.close()

    return flask.render_template(
        "profile.html",
        avatar_src=avatar_src,
        username=username,
        email=email
    )