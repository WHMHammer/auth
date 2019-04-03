import flask
from simplejson import dumps
from time import time

from .. import auth


@auth.bp.route("/verify",methods=("GET","POST"))
def verify():
    if flask.request.method=="GET":
        # check session
        
        
        return flask.render_template(
            "template.html",
            title="Verify",
            action_name="verify",
            ctrl_script_src="verify.js"
        )
    
    
    elif flask.request.method=="POST":
        form=flask.request.get_json()
        try:
            username=str(form["username"])
            response=str(form["response"])
            email=str(form["email"])
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
        
        cur.execute("select password_hash,challenge from users where username=%s and email=%s and status=%s limit 1;",(username,email,"unverified"))
        try:
            password_hash,challenge=cur.fetchone()
        except TypeError:
            conn.close()
            return "{}",403,{"Content-Type":"application/json"}
        
        if response!=auth.hash_r(challenge,password_hash):
            conn.close()
            return "{}",403,{"Content-Type":"application/json"}
        
        cur.execute("update users set status=%s,last_login_time=%s,challenge=%s where username=%s;",("verified",int(time()),auth.generate_salt(),username))
        
        conn.commit()
        conn.close()
        
        
        auth.send_email(auth.NOREPLY,email,"Your registration at %s is verified"%auth.PROJECTNAME,"<p>Dear %s:</p><br/><p>Your registration at %s is verified. Have fun!</p><br/><p>Best rgards,</p><p>%s</p>"%(username,auth.PROJECTNAME,auth.PROJECTNAME))
        
        
        # session
        
        
        return "{}",{"Content-Type":"application/json"}