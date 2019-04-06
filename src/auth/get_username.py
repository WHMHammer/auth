import flask

from .. import auth


@auth.bp.route("/get_username",methods=("GET","POST"))
def get_username():
    # front-end
    if flask.request.method=="GET":
        if auth.get_client_session():
            return flask.redirect("/")
        return flask.render_template(
            "template.html",
            title="Forgot username",
            action_name="submit",
            ctrl_script_src="get_username.js"
        )
    
    
    # back-end
    elif flask.request.method=="POST":
        form=flask.request.get_json()
        try:
            email=str(form["email"]).lower()
        except (KeyError,TypeError):
            return "{}",400,{"Content-Type":"application/json"}
        
        if not(
            auth.check_email(email)
        ):
            return "{}",400,{"Content-Type":"application/json"}
        
        conn=auth.connectDB()
        cur=conn.cursor()
        
        cur.execute("select username from users where email=%s and status=%s limit 1;",(email,"verified"))
        try:
            username=cur.fetchone()[0]
        except TypeError:
            pass
        else:
            auth.send_email(auth.NOREPLY,email,"Your username at %s"%auth.PROJECTNAME,"<p>Your username at %s is:</p><p>%s</p><br/><p>Best regards,</p><p>%s</p>"%(auth.PROJECTNAME,username,auth.PROJECTNAME))
        
        conn.close()
        
        return "{}",{"Content-Type":"application/json"}