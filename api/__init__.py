import flask

app = flask.Flask(__name__)

from auth import bp as auth_bp
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
