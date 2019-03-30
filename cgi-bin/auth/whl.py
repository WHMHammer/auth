import cgi
import json
import re
import smtplib
import traceback
import mysql.connector as sql
from hashlib import sha3_512 as hash_method
from io import TextIOWrapper
from os import environ
from random import choice
from sys import stdin

# project information:
PROJECTNAME="Your Project name"    # change this
DOMAIN="your.domain"    # change this
DEVELOPEREMAIL="developer@email.address"    # change this

# database:
DBUSER="database_username"    # change this
DBPASSWORD="database_password"    # change this
DBNAME="database_name"    # change this

USERNAMEMAXLENGTH=64
SALTLENGTH=16
PASSWORDHASHLENGTH=128
EMAILMAXLENGTH=64

def connectDB():
    return sql.connect(
        user=DBUSER,
        password=DBPASSWORD,
        host="localhost",
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
    "smtp_server":"smtp.server",    # change this
    "port":-1,    # change this
    "address":"noreply@email.address",    # change this
    "token":"email_password_or_token"    # change this
}

# get request information
def check_request_method(methods):
    if isinstance(methods,str):
        methods={methods}
    if environ.get("REQUEST_METHOD") not in methods:
        print("Status: 405")
        print("Allow: %s"%(", ".join(methods)))
        print()
        print("{}")
        exit()

def get_form():
    content_type=environ.get("CONTENT_TYPE","application/x-www-form-urlencoded")
    if re.match(r"^application/json",content_type):
        return json.loads(get_request_body(),encoding="utf8")
    
    return get_form_x_www_form_urlencoded()

def get_form_x_www_form_urlencoded():
    form={}
    field_storage=cgi.FieldStorage()
    for i in field_storage:
        form[i]=field_storage.getvalue(i)
    return form

def get_request_body():
    content_length=int(environ.get("CONTENT_LENGTH"))
    return stdin.read(content_length).encode("utf8","surrogateescape").decode("utf8")
    # Don't replace the code above with the following line or UnicodeEncodeError may occur elsewhere:
    #     return stdin.read(content_length)

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
    s=args[-1]
    for i in range(len(args)-2,-1,-1):
        b=(args[i]+s).encode("utf8")
        h=hash_method(b)
        s=h.hexdigest()
    return s

# utility
def debug(func):
    def foo():
        try:
            func()
        except Exception as e:
            print("Status: 500")
            print()
            err_msg=""
            for i in traceback.format_tb(e.__traceback__):
                err_msg+="<p>%s</p>"%i
            err_msg+="<p>%s</p>"%repr(e)
            send_email(NOREPLY,DEVELOPEREMAIL,"An unexpected error occured at %s"%PROJECTNAME,err_msg)
    return foo

def add_auth_cookie(username):
    # needs implementing
    pass