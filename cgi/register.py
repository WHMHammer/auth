#!/usr/bin/python3
import MySQLdb as sql
import whl    # a customized script
from hashlib import sha512
from json import dumps
from os import environ

try:
    print("Content-Type: application/json")

    if environ.get("REQUEST_METHOD")!="POST":
        print(whl.USE_POST_METHOD)
        exit()

    form=whl.get_form()

    try:
        username=form["username"]
        salt=form["salt"]
        password_hash=form["hash"]
        email=form["email"]
        family_name=form.get("family_name")
        given_name=form.get("given_name")
    except KeyError:
        print(whl.MISSING_PARAMETER)
        exit()

    if not username.isalnum() or len(username)>64:
        print("Status: 400")
        print()
        print(dumps({"status":"illegal username"}))
        exit()

    if not salt.isalnum() and len(salt)==32:
        print("Status: 400")
        print()
        print(dumps({"status":"use 32-digit alnum salt"}))
        exit()

    if not password_hash.isalnum() and len(password_hash)==128:
        print(whl.USE_SHA512)
        exit()

    if "@" not in email or len(email)>54:
        print("Status: 400")
        print()
        print(dumps({"status":"illegal email address"}))
        exit()

    if len(family_name)>32 or len(given_name)>32:
        print("Status: 400")
        print()
        print(dumps({"status":"true name too long"}))
        exit()

    conn=sql.connect(whl.DBHOST,whl.DBUSER,whl.DBPASSWORD,whl.DBNAME)
    cur=conn.cursor()

    try:
        cur.execute("insert into users(email) values(%s);",(email,))
    except sql.IntegrityError:
        conn.close()
        print("Status: 400")
        print()
        print(dumps({"status":"email address already been registered"}))
        exit()

    try:
        cur.execute("update users set username=%s where email=%s;",(username,email))
    except sql.IntegrityError:
        conn.close()
        print("Status: 400")
        print()
        print(dumps({"status":"username already been registered"}))
        exit()

    challenge=whl.rand32()
    cur.execute("update users set password_hash=%s,salt=%s,challenge=%s,surname=%s,familyname=%s where email=%s;",(password_hash,salt,challenge,email,surname,familyname))

    verify_url="https://%s/cgi/verify.py?login=%s&response=%s"%(whl.DOMAIN,username,challenge)
    whl.send_email(whl.NOREPLY,email,"Verify your registration at Cantaloupe","<p>Hello, dear %s:</p><br/><p>Please click <a href=\"%s\">here</a> or paste the following url to your web browser to verify your registration.</p><br/><p>%s</p><br/><p>Best regards,</p><br/><p>the Cantaloupe team</p>"%(username,verify_url)

    conn.commit()
    conn.close()

    print()
    print(dumps({"status":"success"}))
except Exception as e:
    print("Status: 500")
    print()
    print(dumps({
        "status":"unexpected error",
        "error_message":repr(e)
    }))