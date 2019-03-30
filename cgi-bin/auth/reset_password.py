#!/usr/bin/python3
import whl    # a customized script
from json import dumps
from urllib.parse import quote

@whl.debug
def reset_password():
    print("Content-Type: application/json")
    
    whl.check_request_method("POST")
    form=whl.get_form()
    
    try:
        username=form["username"]
        email=form["email"]
        response=form["response"]
        salt=form["salt"]
        password_hash=form["password_hash"]
    except KeyError:
        print("Status: 400")
        print()
        print("{}")
        return
    
    try:
        bytes(email,"ascii")
    except UnicodeEncodeError:
        print("Status: 400")
        print()
        print("{}")
        return
    
    if (
        username=="" or len(username)>whl.USERNAMEMAXLENGTH or
        len(salt)!=whl.SALTLENGTH or
        len(password_hash)!=whl.PASSWORDHASHLENGTH or
        len(email)>whl.EMAILMAXLENGTH
    ):
        print("Status: 400")
        print()
        print("{}")
        return
    
    conn=whl.connectDB()
    cur=conn.cursor()
    
    cur.execute("select * from users where username=%s and email=%s and challenge=%s and status=%s limit 1;",(username,email,response,"verified"))
    if cur.fetchone() is not None:
        cur.execute("update users set salt=%s,password_hash=%s,chellenge=%s where username=%s;",(salt,password_hash,whl.generate_salt(),username))
        
        conn.commit()
        
        whl.send_email(whl.NOREPLY,email,"You have successfully changed your password!","<p>Hello, dear %s:</p><p>You have successfully changed your password!</p><br/><p>Best regards,</p><p>%s</p>"%(username,whl.PROJECTNAME))
    
    conn.close()
    
    whl.add_auth_cookie(username)
    
    print()
    print("{}")

if __name__=="__main__":
    reset_password()