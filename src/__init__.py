import flask

def create_app():
    app=flask.Flask(__name__)
    app.secret_key="secret_key"
    
    @app.route("/",methods=("GET",))
    def root():
        return flask.redirect("/auth/login")
    
    # register blueprints    
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app