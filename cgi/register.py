#!/usr/bin/python3
import whl    # a customized script
from json import dumps
from urllib.parse import quote

import traceback

def register():
    print("Content-Type: application/json")
    
    whl.check_request_method("POST")
    form=whl.get_form()
    
    try:
        username=form["username"]
        salt=form["salt"]
        password_hash=form["password_hash"]
        email=form["email"]
    except KeyError:
        print("Status: 400")
        print()
        exit()
    
    if (
        username=="" or len(username)>whl.USERNAMEMAXLENGTH or
        len(salt)!=whl.SALTLENGTH or
        len(password_hash)!=whl.PASSWORDHASHLENGTH or
        len(email)>64
    ):
        print("Status: 400")
        print()
        exit()
    
    conn=whl.sql.connect(whl.DBHOST,whl.DBUSER,whl.DBPASSWORD,whl.DBNAME)
    cur=conn.cursor()
    
    err=False
    err_msg=[]
    
    cur.execute("select * from users where email=%s and status!=%s",(email,"unverified"))
    if cur.fetchone() is not None:
        err=True
        err_msg.append("email registered")
    
    cur.execute("select * from users where username=%s and status!=%s",(username,"unverified"))
    if cur.fetchone() is not None:
        err=True
        err_msg.append("username registered")
    
    if err:
        print("Status: 403")
        print()
        print(dumps({"err_msg":err_msg}))
        exit()
    
    challenge=whl.rand32()
    
    cur.execute("insert into users(username,salt,password_hash,email,challenge) values(%s,%s,%s,%s,%s);",(username,salt,password_hash,email,challenge))
    
    try:
        verify_url="https://%s/cgi/verify.py?login=%s&response=%s"%(whl.DOMAIN,quote(username),challenge)
        whl.send_email(whl.NOREPLY,email,"Verify your registration at %s","<p>Hello, dear %s:</p><br/><p>Please click <a href=\"%s\">here</a> or paste the following url to your web browser to verify your registration.</p><br/><p>%s</p><br/><p>Best regards,</p><br/><p>the %S team</p>"%(whl.PROJECTNAME,username,verify_url,verify_url,whl.PROJECTNAME)
    except whl.smtplib.SMTPRecipientsRefused:
        conn.commit()
        print("Status: 401")
        print()
        print(print(dumps({"err_msg":["invalid email"]})))
        exit()
    
    conn.commit()
    conn.close()

    print()

if __name__=="__main__":
    #register()
    #"""
    try:
        register()
    except Exception as e:
        print("Status: 500")
        print()
        print(dumps({
            "err_msg":traceback.format_tb(e.__traceback__)
        }))
    #"""