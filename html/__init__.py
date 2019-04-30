import flask

app = flask.Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path=""
)


@app.route("/", methods=("GET",))
def root():
    return flask.render_template(
        "root.html",
        title="Home"
    )

# register blueprints
from auth import bp as auth_bp
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
