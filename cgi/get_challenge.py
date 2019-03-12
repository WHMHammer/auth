#!/usr/bin/python3
import whl    # a customized script
from json import dumps

def get_challenge():
    print("Content-Type: application/json")
    
    whl.check_request_method("POST")
    
    form=whl.get_form()
    
    try:
        username=form["username"]
    except KeyError:
        print("Status: 400")
        print()
        exit()
    
    if len(username)>whl.USERNAMEMAXLENGTH:
        print("Status: 400")
        print()
        exit()
    
    conn=whl.sql.connect(whl.DBHOST,whl.DBUSER,whl.DBPASSWORD,whl.DBNAME)
    cur=conn.cursor()
    
    cur.execute("select salt from users where username=%s and status=%s;",(username,"verified"))
    try:
        salt=cur.fetchone()[0]
    except TypeError:
        conn.close()
        print("Status: 404")
        print()
        exit()
    
    challenge=whl.rand32()
    
    cur.execute("update users set challenge=%s where username=%s;",(challenge,username))
    
    conn.commit()
    conn.close()
    
    print()
    print(dumps({
        "salt":salt,
        "challenge":challenge
    }))

if __name__=="__main__":
    #get_challenge()
    #"""
    try:
        get_challenge()
    except Exception as e:
        print("Status: 500")
        print()
        print(dumps({
            "err_msg":traceback.format_tb(e.__traceback__)
        }))
    #"""