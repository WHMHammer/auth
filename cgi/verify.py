#!/usr/bin/python3
import whl    # a customized script
from time import time
from urllib.parse import unquote

import traceback

def verify():
    print("Content-Type: application/json")
    
    whl.check_request_method("GET")
    form=whl.get_form()
    
    try:
        username=unquote(form["username"])
        response=form["response"]
    except KeyError:
        print("Status: 400")
        print()
        exit()
    
    if len(username)>whl.USERNAMEMAXLENGTH or len(response)!=whl.CHALLENGELENGTH:
        print("Status: 400")
        print()
        exit()
    
    conn=whl.sql.connect(whl.DBHOST,whl.DBUSER,whl.DBPASSWORD,whl.DBNAME)
    cur=conn.cursor()
    
    cur.execute("select status,challenge from users where username=%s;",(username,))
    try:
        status,challenge=cur.fetchone()
    except TypeError:
        conn.close()
        print("Status: 404")
        print()
        exit()
    
    if status!="unverified" or response!=challenge:
        conn.close()
        print("Status: 403")
        print()
        exit()
    
    cur.execute("update users set status=%s,last_login_time=%s,challenge=%s where username=%s;",("verified",int(time()),whl.rand32(),username))
    
    conn.commit()
    conn.close()
    
    print()

if __name__=="__main__":
    #verify()
    #"""
    try:
        verify()
    except Exception as e:
        print("Status: 500")
        print()
        print(dumps({
            "err_msg":traceback.format_tb(e.__traceback__)
        }))
    #"""