#!/usr/bin/python3
import MySQLdb as sql
import whl    # a customized script
from json import dumps
from os import environ

try:
    print("Content-Type: application/json")

    if environ.get("REQUEST_METHOD")!="POST":
        print(whl.USE_POST_METHOD)
        exit()

    form=whl.get_form()

    try:
        login=form["login"]
    except KeyError:
        print(whl.MISSING_PARAMETER)
        exit()

    if not login.isalnum() and "@" not in login:
        print(whl.ILLEGAL_LOGIN)
        exit()

    conn=sql.connect(whl.DBHOST,whl.DBUSER,whl.DBPASSWORD,whl.DBNAME)
    cur=conn.cursor()

    if "@" in login:
        cur.execute("select salt,last_login_time,challenge from users where email=%s;",(login,))
    else:
        cur.execute("select salt,last_login_time,challenge from users where username=%s;",(login,))
    try:
        salt,last_login_time,challenge=cur.fetchone()
    except TypeError:
        conn.close()
        print(whl.USER_NOT_FOUND)
        exit()

    if last_login_time==0:
        conn.close()
        print(whl.USER_NOT_VERIFIED)
        exit()

    challenge=whl.rand32()

    if "@" in login:
        cur.execute("update users set challenge=%s where email=%s;",(challenge,login))
    else:
        cur.execute("update users set challenge=%s where username=%s;",(challenge,login))

    conn.commit()
    conn.close()

    print()
    print(dumps({
        "status":"success",
        "salt":salt,
        "challenge":challenge
    }))
except Exception as e:
    print("Status: 500")
    print()
    print(dumps({
        "status":"unexpected error",
        "error_message":repr(e)
    }))