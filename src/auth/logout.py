import flask

from .. import auth


@auth.bp.route("/logout",methods=("GET","POST"))
def logout():
    if flask.request.method=="GET":
        return """<script src="js/auth.js"></script><script>
            var rq=new XMLHttpRequest();
            rq.onreadystatechange=function () {
                if (this.readyState==4) {
                    remove_login();
                    window.location.replace("/");
                }
            };
            rq.open("POST","/auth/logout",true);
            rq.setRequestHeader("Content-Type","application/json");
            rq.send();
        </script>"""
    else:
        if auth.check_client_session():
            conn=auth.connectDB()
            cur=conn.cursor()
            
            cur.execute("update users set session=%s where id=%s;",(auth.generate_salt(),flask.session.get("user_id")))
            
            conn.commit()
            conn.close()
            
            flask.session.pop("user_id")
            flask.session.pop("session")
            
        return "{}",{"Content-Type":"application/json"}