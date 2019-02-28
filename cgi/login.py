#!/usr/bin/python3
import MySQLdb as sql
import whl    # a customized script
from hashlib import sha512
from json import dumps
from os import environ
from time import time

try:
    print("Content-Type: application/json")

    if environ.get("REQUEST_METHOD")!="POST":
        print(whl.USE_POST_METHOD)
        exit()

    form=whl.get_form()

    try:
        login=form["login"]
        response=form["response"]
    except KeyError:
        print(whl.MISSING_PARAMETER)
        exit()

    if not login.isalnum() and "@" not in login:
        print(whl.ILLEGAL_LOGIN)
        exit()

    if not response.isalnum() and len(password_hash)!=128:
        print(whl.USE_SHA512)
        exit()

    conn=sql.connect(whl.DBHOST,whl.DBUSER,whl.DBPASSWORD,whl.DBNAME)
    cur=conn.cursor()

    if "@" in login:
        cur.execute("select password_hash,last_login_time,challenge from users where email=%s;",(login,))
    else:
        cur.execute("select password_hash,last_login_time,challenge from users where username=%s;",(login,))
    try:
        password_hash,last_login_time,challenge=cur.fetchone()
    except TypeError:
        conn.close()
        print(whl.USER_NOT_FOUND)
        exit()

    if last_login_time==0:
        conn.close()
        print(whl.USER_NOT_VERIFIED)
        exit()

    s=bytes(challenge+password_hash,"ascii")
    h=sha512(s)
    if h.hexdigest()!=response:
        conn.close()
        print(whl.FAIL)
        exit()

    if "@" in login:
        cur.execute("update users set last_login_time=%s,challenge=%s where email=%s;",(int(time()),whl.rand32(),login))
    else:
        cur.execute("update users set last_login_time=%s,challenge=%s where username=%s;",(int(time()),whl.rand32(),login))

    conn.commit()
    conn.close()

    #Add cookie

    print()
    print(dumps({"status":"success"}))
except Exception as e:
    print("Status: 500")
    print()
    print(dumps({
        "status":"unexpected error",
        "error_message":repr(e)
    }))