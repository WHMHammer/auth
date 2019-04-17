import flask
from time import time

import auth


@auth.bp.route("/login",methods=("GET","POST"))
def login():
    # front-end
    if flask.request.method=="GET":
        if auth.check_client_session():
            return flask.redirect("/")
        return flask.render_template(
            "auth.html",
            title="Login",
            action_name="login",
            ctrl_script_src="login.js"
        )
    
    
    # back-end
    elif flask.request.method=="POST":
        form=flask.request.get_json()
        try:
            username=str(form["username"])
            response=str(form["response"])
        except (KeyError,TypeError):
            return "{}",400,{"Content-Type":"application/json"}
        
        if not(
            auth.check_username(username) and
            auth.check_response(response)
        ):
            return "{}",400,{"Content-Type":"application/json"}
        
        conn=auth.connectDB()
        cur=conn.cursor()
        
        cur.execute("select password_hash,challenge from users where username=%s and status=%s limit 1;",(username,"verified"))
        try:
            password_hash,challenge=cur.fetchone()
        except TypeError:
            return "{}",404,{"Content-Type":"application/json"}
        
        if response!=auth.hash_r(challenge,password_hash):
            conn.close()
            return "{}",403,{"Content-Type":"application/json"}
        
        cur.execute("update users set last_login_time=%s,challenge=%s where username=%s;",(int(time()),auth.generate_salt(),username))
        
        conn.commit()
        conn.close()
        
        auth.set_client_session(username)
        
        return auth.login_info(),{"Content-Type":"application/json"}