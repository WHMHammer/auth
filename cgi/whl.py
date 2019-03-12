import cgi
import json
import smtplib
import mysql.connector as sql
from hashlib import sha3_512 as hash_method
from os import environ
from random import choice
from sys import stdin

# project setting:
PROJECTNAME="your project name"

# server setting:
DOMAIN="your.domain"

# database setting:
DBHOST="you.database.host"
DBUSER="your_database_user"
DBPASSWORD="your_database_password"
DBNAME="your_database_name"

USERNAMEMAXLENGTH=64
SALTLENGTH=32
PASSWORDHASHLENGTH=128
EMAILMAXLENGTH=64
CHALLENGELENGTH=32

# email box information:
# be taken as the first parameter (sender) in "send_email()" defined below
NOREPLY={
    "smtp_server":"smtp.gmail.com",
    "port":465,
    "address":"noreply.your.project@gmail.com",
    "token":"your_email_box_token"
}

# get request information
def check_request_method(**methods):
    if environ.get("REQUEST_METHOD") not in methods:
        print("Status: 405")
        print("Allow: %s"%(", ".join(methods)))
        print()
        exit()

def get_form():
    return {
        "application/x-www-form-urlencoded":get_form_x_www_form_urlencoded,
        "application/json":get_form_json
    }.get(get_request_method(),dict())()

def get_form_x_www_form_urlencoded():
    form={}
    field_storage=cgi.FieldStorage()
    for i in field_storage:
        form[i]=field_storage.getvalue(i)
    return form

def get_form_json():
    l=int(environ.get("CONTENT_LENGTH"))
    return json.loads(stdin.read(l))

#utilities
def rand32():
    # generate a string matching the regular expression "^([0-9]|[a-z]|[A-Z]){32}$"
    alnum="01234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    r=""
    for i in range(32):
        r+=choice(alnum)
    return r

def send_email(sender,to,subject=,body):
    # sender is a dictionary storing email box information
    # to is an email address in str
    # body is an HTML string
    # take NOREPLY defined above as an example
    with smtplib.SMTP_SSL(sender.get("smtp_server"),sender.get("port")) as conn:
        conn.login(sender.get("address"),sender.get("token"))
        conn.sendmail(sender.get("address"),to,"sender: %s\nTo: %s\nSubject: %s\nContent-Type: text/html\n\n%s"%(sender.get("address"),to,subject,body))

def hash_r(*args):
    # hash recursively
    # e.g.
    #  hash_r(challenge,salt,secret)
    # =hash(challenge+hash(salt+secret))
    s=args[-1]
    for i in range(len(args)-2,-1,-1):
        b=bytes(args[i]+s,"utf8")
        h=hash_method(b)
        s=h.hexdigest()
    return s