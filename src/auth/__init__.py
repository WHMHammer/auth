import flask
import smtplib
import mysql.connector as sql
from hashlib import sha3_512 as hash_method
from random import choice


bp=flask.Blueprint("auth",__name__,url_prefix="/auth",template_folder="html",static_folder="static")

@bp.route("/",methods=("GET",))
def auth():
    return flask.redirect("login")


# views
from . import register
from . import verify
from . import get_challenge
from . import login
from . import get_username


# project information:
PROJECTNAME="project name"
DOMAIN="project.domain"
DEVELOPEREMAIL="developer@email.address"


# database:
DBUSER="db_user"
DBPASSWORD="db_password"
DBHOST="db_host"
DBNAME="db_name"

USERNAMEMAXLENGTH=64
SALTLENGTH=16
PASSWORDHASHLENGTH=128
EMAILMAXLENGTH=64

def connectDB():
    return sql.connect(
        user=DBUSER,
        password=DBPASSWORD,
        host=DBHOST,
        database=DBNAME
    )


# email
def send_email(sender,to,subject,body):
    # sender is a dictionary storing email box information
    # to is an email address in str
    # body is an HTML string
    # take NOREPLY defined below as an example
    with smtplib.SMTP_SSL(sender.get("smtp_server"),sender.get("port")) as conn:
        conn.login(sender.get("address"),sender.get("token"))
        conn.sendmail(sender.get("address"),to,bytes("Sender: %s\nTo: %s\nSubject: %s\nContent-Type: text/html\n\n%s"%(sender.get("address"),to,subject,body),"utf8"))

NOREPLY={
    "smtp_server":"smtp.server",
    "port":-1,
    "address":"noreply@email.address",
    "token":"token_or_password"
}


# check request entries (for database)
def check_username(username):
    return bool(username) and len(username)<=USERNAMEMAXLENGTH

def check_salt(salt):
    return len(salt)==SALTLENGTH

def check_response(response):
    return len(response)==PASSWORDHASHLENGTH

def check_email(email):
    return len(email)<=EMAILMAXLENGTH


# hash
def rand_str(length):
    alnum="01234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    r=""
    for i in range(length):
        r+=choice(alnum)
    return r

def generate_salt():
    return rand_str(SALTLENGTH)

def hash_r(*args):
    # hash recursively
    # e.g.
    #   hash_r(challenge,salt,secret)
    # = hash(challenge+hash(salt+secret))
    if len(args)==1:
        h=hash_method(args[0])
        return h.hexdigest()
    s=args[-1]
    for i in range(len(args)-2,-1,-1):
        b=(args[i]+s).encode("utf8")
        h=hash_method(b)
        s=h.hexdigest()
    return s