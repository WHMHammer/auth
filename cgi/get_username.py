#!/usr/bin/python3
import whl    # a customized script
from json import dumps

def get_username():
    print("Content-Type: application/json")
    
    whl.check_request_method("POST")
    
    form=whl.get_form()
    
    try:
        email=form["email"]
    except KeyError:
        print("Status: 400")
        print()
        exit()
    
    if len(email)>whl.EMAILMAXLENGTH:
        print("Status: 400")
        print()
        exit()
    
    conn=whl.sql.connect(whl.DBHOST,whl.DBUSER,whl.DBPASSWORD,whl.DBNAME)
    cur=conn.cursor()
    
    cur.execute("select username from users where email=%s and status=%s;",(email,"verified"))
    try:
        username=cur.fetchone()[0]
    except TypeError:
        conn.close()
        print("Status: 404")
        print()
        exit()
    
    conn.close()
    
    print()
    print(dumps({
        "username":username
    }))

if __name__=="__main__":
    #get_username()
    #"""
    try:
        get_username()
    except Exception as e:
        print("Status: 500")
        print()
        print(dumps({
            "err_msg":traceback.format_tb(e.__traceback__)
        }))
    #"""