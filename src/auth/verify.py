import flask
from time import time

from .. import auth


@auth.bp.route("/verify",methods=("GET","POST"))
def verify():
    # front-end
    if flask.request.method=="GET":
        if auth.check_client_session():
            return flask.redirect("/")
        return flask.render_template(
            "auth.html",
            title="Verify",
            action_name="verify",
            ctrl_script_src="verify.js"
        )
    
    
    # back-end
    elif flask.request.method=="POST":
        form=flask.request.get_json()
        try:
            username=str(form["username"])
            response=str(form["response"])
            email=str(form["email"]).lower()
        except (KeyError,TypeError):
            return "{}",400,{"Content-Type":"application/json"}
        
        if not(
            auth.check_username(username) and
            auth.check_response(response) and
            auth.check_email(email)
        ):
            return "{}",400,{"Content-Type":"application/json"}
        
        conn=auth.connectDB()
        cur=conn.cursor()
        
        cur.execute("select password_hash,session from users where username=%s and email=%s and status=%s limit 1;",(username,email,"unverified"))
        try:
            password_hash,session=cur.fetchone()
        except TypeError:
            conn.close()
            return "{}",403,{"Content-Type":"application/json"}
        
        if response!=auth.hash_r(session,password_hash):
            conn.close()
            return "{}",403,{"Content-Type":"application/json"}
        
        session=auth.generate_salt()
        
        cur.execute("update users set status=%s,last_login_time=%s,session=%s where username=%s;",("verified",int(time()),session,username))
        
        conn.commit()
        conn.close()
        
        auth.send_email(auth.NOREPLY,email,"Your registration at %s is verified"%auth.PROJECTNAME,"<p>Dear %s:</p><br/><p>Your registration at %s is verified. Have fun!</p><br/><p>Best rgards,</p><p>%s</p>"%(username,auth.PROJECTNAME,auth.PROJECTNAME))
        
        auth.set_client_session(username)
        
        return auth.login_info(),{"Content-Type":"application/json"}