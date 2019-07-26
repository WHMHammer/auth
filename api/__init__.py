from lib import *

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = secret_key


@app.before_request
def before_all():
    if flask.request.method == "OPTIONS":
        return "{}"
    elif flask.request.method != "GET":
        flask.g.form = flask.request.get_json()
    else:
        flask.g.form = flask.request.args

    flask.g.db = connect_db()


@app.after_request
def after_all(rp):
    db = flask.g.pop("db", None)
    if db is not None:
        db.close()
    rp.headers.set("Access-Control-Allow-Origin", "*")
    rp.headers.set("Access-Control-Allow-Methods", "OPTIONS, GET, POST, PUT, DELETE")
    rp.headers.set("Access-Control-Allow-Headers", "Content-Type")
    rp.headers.set("Content-Type", "application/json")
    return rp


from auth import bp as auth_bp
app.register_blueprint(auth_bp)

from event import bp as event_bp
app.register_blueprint(event_bp)
