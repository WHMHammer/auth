#!/usr/bin/python3
import whl    # a customized script
from json import dumps
from time import time

@whl.debug
def login():
    print("Content-Type: application/json")
    
    whl.check_request_method("POST")
    form=whl.get_form()
    
    try:
        username=form["username"]
        response=form["response"]
    except KeyError:
        print("Status: 400")
        print()
        print("{}")
        exit()
    
    if len(username)>whl.USERNAMEMAXLENGTH or len(response)!=whl.PASSWORDHASHLENGTH:
        print("Status: 400")
        print()
        print("{}")
        exit()
    
    conn=whl.connectDB()
    cur=conn.cursor()
    
    cur.execute("select password_hash,challenge from users where username=%s and status=%s limit 1;",(username,"verified"))
    try:
        password_hash,challenge=cur.fetchone()
    except TypeError:
        conn.close()
        print("Status: 404")
        print()
        print("{}")
        exit()
    
    if response!=whl.hash_r(challenge,password_hash):
        conn.close()
        print("Status: 403")
        print()
        print("{}")
        exit()
    
    cur.execute("update users set last_login_time=%s,challenge=%s where username=%s;",(int(time()),whl.generate_salt(),username))
    
    conn.commit()
    conn.close()
    
    whl.add_auth_cookie(username)
    
    print()
    print("{}")

if __name__=="__main__":
    login()