import flask
from simplejson import dumps
from time import time

from .. import auth


@auth.bp.route("/login",methods=("GET","POST"))
def login():
    if flask.request.method=="GET":
        # check session
        
        
        return flask.render_template(
            "template.html",
            title="Login",
            action_name="login",
            ctrl_script_src="login.js"
        )
    
    
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
        
        
        # session
        
        
        return "{}",{"Content-Type":"application/json"}