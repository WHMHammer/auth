#!/usr/bin/python3
import whl    # a customized script
from json import dumps
from time import time

import traceback

@whl.debug
def verify():
    print("Content-Type: application/json")
    
    whl.check_request_method("POST")
    form=whl.get_form()
    
    try:
        username=form["username"]
        response=form["response"]
        email=form["email"]
    except KeyError:
        print("Status: 400")
        print()
        print("{}")
        return
    
    if (
        len(username)>whl.USERNAMEMAXLENGTH or
        len(response)!=whl.PASSWORDHASHLENGTH or
        len(email)>whl.EMAILMAXLENGTH
    ):
        print("Status: 400")
        print()
        print("{}")
        return
    
    conn=whl.connectDB()
    cur=conn.cursor()
    
    cur.execute("select password_hash,challenge from users where username=%s and email=%s and status=%s;",(username,email,"unverified"))
    try:
        password_hash,challenge=cur.fetchone()
    except TypeError:
        conn.close()
        print("Status: 403")
        print()
        print("{}")
        return
    
    if response!=whl.hash_r(challenge,password_hash):
        conn.close()
        print("Status: 403")
        print()
        print("{}")
        return
    
    cur.execute("update users set status=%s,last_login_time=%s,challenge=%s where username=%s;",("verified",int(time()),whl.generate_salt(),username))
    
    conn.commit()
    conn.close()
    
    whl.send_email(whl.NOREPLY,email,"Your registration at %s is verified"%whl.PROJECTNAME,"<p>Dear %s:</p><br/><p>Your registration at %s is verified. Have fun!</p><br/><p>Best rgards,</p><p>%s</p>"%(username,whl.PROJECTNAME,whl.PROJECTNAME))
    
    #Add cookie
    
    print()
    print("{}")

if __name__=="__main__":
    verify()