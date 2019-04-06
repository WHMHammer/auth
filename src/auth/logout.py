import flask

from .. import auth


@auth.bp.route("/logout",methods=("GET",))
def logout():
    flask.session.clear()
    return flask.redirect(flask.request.args.get("r","/"))