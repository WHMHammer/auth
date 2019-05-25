import flask
import smtplib
import mysql.connector as sql
from functools import wraps
from hashlib import sha3_512 as hash_method
from random import choice
from simplejson import dumps
from time import time

# blueprint
bp = flask.Blueprint("auth", __name__, url_prefix="/auth")

# project information:
PROJECTNAME = "WHMHammer's website"
DOMAIN = "www.whmhammer.com"
DEVELOPEREMAIL = "whmhammer@gmail.com"


def cors(url):
    def foo(func):
        @bp.route(url, methods=("POST", "OPTIONS"))
        @wraps(func)
        def bar():
            if flask.request.method == "OPTIONS":
                return "{}", {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Content-Type": "application/json"
                }
            rp = flask.make_response(func())
            rp.headers.set("Access-Control-Allow-Origin", "*")
            rp.headers.set("Content-Type", "application/json")
            return rp
        return bar
    return foo

# views
from . import register
from . import verify
from . import get_challenge
from . import login
from . import get_username
from . import request_password
from . import reset_password
from . import logout
from . import update_username
from . import update_email
from . import update_avatar

# database:
DBUSER = "Nope!"
DBPASSWORD = "Not here!"
DBHOST = "db.whmhammer.com"
DBNAME = "auth"

USERNAMEMAXLENGTH = 64
SALTLENGTH = 16
PASSWORDHASHLENGTH = 128
EMAILMAXLENGTH = 64
LINKMAXLENGTH = 512

SESSIONEXPIRETIME = 86400   # 86400 seconds == 24 hours


def connectDB():
    return sql.connect(
        user=DBUSER,
        password=DBPASSWORD,
        host=DBHOST,
        database=DBNAME
    )


# email
def send_email(sender, to, subject, body):
    # sender is a dictionary storing email box information
    # to is an email address in str
    # body is an HTML string
    # take NOREPLY defined below as an example
    with smtplib.SMTP_SSL(sender.get("smtp_server"), sender.get("port")) as conn:
        conn.login(sender.get("address"), sender.get("token"))
        conn.sendmail(
            sender.get("address"),
            to,
            bytes("Sender: %s\nTo: %s\nSubject: %s\nContent-Type: text/html\n\n%s" % (
                sender.get("address"),
                to,
                subject,
                body
            ), "utf8")
        )

NOREPLY = {
    "smtp_server": "smtp.gmail.com",
    "port": 465,
    "address": "noreply.whmhammer@gmail.com",
    "token": "No way!"
}


# check request entries (for database)
def check_username(username):
    return bool(username) and len(username) <= USERNAMEMAXLENGTH


def check_salt(salt):
    return len(salt) == SALTLENGTH


def check_response(response):
    return len(response) == PASSWORDHASHLENGTH


def check_email(email):
    return len(email) <= EMAILMAXLENGTH

def check_link(link):
    return len(link) <= LINKMAXLENGTH


# hash
def rand_str(length):
    alnum = "01234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    return "".join([choice(alnum) for i in range(length)])


def generate_salt():
    return rand_str(SALTLENGTH)


def hash_r(*args):
    # hash recursively
    # e.g.
    #   hash_r(challenge,salt,secret)
    # = hash(challenge+hash(salt+secret))
    if len(args) == 1:
        h = hash_method(args[0])
        return h.hexdigest()
    s = args[-1]
    for i in range(len(args)-2, -1, -1):
        b = (args[i]+s).encode("utf8")
        h = hash_method(b)
        s = h.hexdigest()
    return s


# user info
def generate_user_token(username):
    conn = connectDB()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, email, avatar
        FROM users
        WHERE username = %s
        LIMIT 1;
    """, (username,))

    user_id, email, avatar = cur.fetchone()

    session = generate_salt()
    cur.execute("""
        INSERT into sessions
        VALUES(%s,%s,%s);
    """, (user_id, session, int(time())+SESSIONEXPIRETIME))

    conn.commit()
    conn.close()

    return {
        "user_id": user_id,
        "session": session,
        "username": username,
        "email": email,
        "avatar": avatar
    }


def check_user_token():
    user_token = flask.request.get_json().get("user_token")
    try:
        user_id = int(user_token["user_id"])
        session = str(user_token["session"])
    except (KeyError, TypeError):
        return None

    if not check_salt(session):
        return None

    conn = connectDB()
    cur = conn.cursor()

    cur.execute("""
        DELETE from sessions
        WHERE expire_time < %s;
    """, (int(time()),))

    conn.commit()

    cur.execute("""
        SELECT users.username, users.email, users.role
        FROM users RIGHT JOIN sessions
        ON users.id=sessions.user_id
        WHERE users.id=%s AND users.status=%s AND sessions.session=%s
        LIMIT 1;
    """, (user_id, "verified", session))

    try:
        username, email, role = cur.fetchone()
    except TypeError:
        return None

    return {
        "id": user_id,
        "username": username,
        "email": email,
        "role": role
    }
