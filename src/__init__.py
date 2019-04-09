import flask

from . import auth

def create_app():
    app=flask.Flask(
        __name__,
        static_url_path=""
    )
    app.secret_key="secret_key"
    
    @app.route("/",methods=("GET",))
    def root():
        return flask.render_template(
            "root.html",
            title="Root"
        )
    
    # register blueprints
    app.register_blueprint(auth.bp)
    
    return app