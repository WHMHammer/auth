import flask

from .. import auth


@auth.bp.route("/profile",methods=("GET","POST"))
def profile():
    # front-end
    if flask.request.method=="GET":
        pass
    
    
    # back-end
    elif flask.request.method=="POST":
        pass