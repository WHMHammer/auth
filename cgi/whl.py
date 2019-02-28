import cgi
import json
import smtplib
from os import environ
from random import choice
from string import ascii_letters,digits
from sys import stdin

rand32=lambda :"".join([choice(ascii_letters+digits) for i in range(32)])

get_form=lambda :{
        None:lambda :{},
        "application/x-www-form-urlencoded":get_form_x_www_form_urlencoded,
        "application/json":lambda :json.loads(stdin.read(int(environ.get("CONTENT_LENGTH"))))
    }.get(os.environ.get("CONTENT_TYPE"))()

def get_form_x_www_form_urlencoded():
    form={}
    field_storage=cgi.FieldStorage()
    for i in field_storage:
        form[i]=field_storage.getvalue(i)
    return form

def send_email(sender,to,subject,body):
    # sender is a dictionary storing email box information
    # to is an email address in str
    # body is an HTML string
    with smtplib.SMTP_SSL(sender.get("smtp_server"),sender.get("port")) as conn:
        conn.login(sender.get("address"),sender.get("token"))
        conn.sendmail(sender.get("address"),to,"sender: %s\nTo: %s\nSubject: %s\nContent-Type: text/html\n\n%s"%(sender.get("address"),to,subject,body))
        
# server setting:
DOMAIN=""

# database setting:
DBHOST=""
DBUSER=""
DBPASSWORD=""
DBNAME=""

# email box information:
NOREPLY={
    "smtp_server":"smtp.gmail.com",
    "port":465,
    "address":"noreply.name@gmail.com",
    "token":"password"
}

# error message:
USE_POST_METHOD="Status: 405\nAllow: POST\n\n{\"status\": \"use POST method\"}"
MISSING_PARAMETER="Status: 400\n\n{\"status\": \"missing parameter\"}"
USE_SHA512="Status: 400\n\n{\"status\": \"use sha512\"}"
ILLEGAL_LOGIN="Status: 400\n\n{\"status\": \"illegal login\"}"
USER_NOT_FOUND="Status: 404\n\n{\"status\": \"user not found\"}"
FAIL="Status: 403\n\n{\"status\": \"fail\"}"
USER_NOT_VERIFIED="Status: 403\n\n{\"status\": \"user hasn't been verified\"}"