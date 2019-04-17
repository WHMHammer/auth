import flask

import auth

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

if __name__=="__main__":
    app.run(host="0.0.0.0",port=80)