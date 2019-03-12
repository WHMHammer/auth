#!/usr/bin/python3
import whl    # a customized script
from json import dumps
from time import time

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
        exit()
    
    if len(username)>whl.USERNAMEMAXLENGTH or len(response)!=whl.PASSWORDHASHLENGTH:
        print("Status: 400")
        print()
        exit()
    
    conn=sql.connect(whl.DBHOST,whl.DBUSER,whl.DBPASSWORD,whl.DBNAME)
    cur=conn.cursor()
    
    cur.execute("select password_hash,challenge from users where username=%s and status=%s;",(username,"verified"))
    try:
        password_hash,challenge=cur.fetchone()
    except TypeError:
        conn.close()
        print("Status: 404")
        print()
        exit()
    
    if response!=whl.hash_r(challenge,password_hash):
        conn.close()
        print("Status: 403")
        print()
        exit()
    
    cur.execute("update users set last_login_time=%s,challenge=%s where username=%s;",(int(time()),whl.rand32(),username))
    
    conn.commit()
    conn.close()
    
    #Add cookie
    
    print()

if __name__=="__main__":
    #login()
    #"""
    try:
        login()
    except Exception as e:
        print("Status: 500")
        print()
        print(dumps({
            "err_msg":traceback.format_tb(e.__traceback__)
        }))
    #"""