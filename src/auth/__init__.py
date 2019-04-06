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
from . import request_password
from . import reset_password
from . import logout
from . import get_username


# project information:
PROJECTNAME=""
DOMAIN=""
DEVELOPEREMAIL=""


# database:
DBUSER=""
DBPASSWORD=""
DBHOST=""
DBNAME=""

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
    "smtp_server":"",
    "port":0,
    "address":"",
    "token":""
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

# session
def set_client_session(username):
    conn=connectDB()
    cur=conn.cursor()
    
    cur.execute("select id from users where username=%s limit 1;",(username,))
    user_id=cur.fetchone()[0]
    
    session=generate_salt()
    cur.execute("update users set session=%s where username=%s;",(session,username))
    
    conn.commit()
    conn.close()
    
    flask.session["user_id"]=user_id
    flask.session["session"]=session

def get_client_session():
    user_id=flask.session.get("user_id")
    session=flask.session.get("session")
    if user_id is None or session is None:
        return False
    
    conn=connectDB()
    cur=conn.cursor()
    
    cur.execute("select * from users where id=%s and status=%s and session=%s limit 1;",(user_id,"verified",session))
    
    if cur.fetchone() is not None:
        conn.close()
        return True
    
    conn.close()
    return False