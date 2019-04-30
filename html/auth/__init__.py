import flask
import smtplib
import mysql.connector as sql
from hashlib import sha3_512 as hash_method
from random import choice
from simplejson import dumps


bp = flask.Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder="templates",
    static_folder="static",
    static_url_path=""
)


@bp.route("/", methods=("GET",))
def auth():
    return flask.redirect("login")


# views
from . import register
from . import verify
from . import login
from . import get_username
from . import request_password
from . import reset_password
from . import logout
from . import profile
