#!/usr/bin/python3
import whl    # a customized script
from json import dumps
from urllib.parse import quote

@whl.debug
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
        conn.close()
        print("Status: 403")
        print()
        print(dumps({"err_msg":err_msg}))
        return
    
    challenge=whl.generate_salt()
    
    cur.execute("delete from users where username=%s or email=%s;",(username,email))
    cur.execute("insert into users(username,salt,password_hash,email,challenge) values(%s,%s,%s,%s,%s);",(username,salt,password_hash,email,challenge))
    
    try:
        verify_url="https://%s/auth/verify.html"%(whl.DOMAIN)
        whl.send_email(whl.NOREPLY,email,"Verify your registration at %s"%whl.PROJECTNAME,"<p>Hello, dear %s:</p><p>Your verification code is:</p><p><code>%s</code></p>Please click <a href=\"%s\">here</a> or paste the following url to your web browser to verify your registration:</p><p>%s</p><br/><p>Best regards,</p><p>%s</p>"%(username,challenge+salt,verify_url,verify_url,whl.PROJECTNAME))
    except whl.smtplib.SMTPRecipientsRefused:
        conn.close()
        print("Status: 403")
        print()
        print(dumps({"err_msg":["invalid email"]}))
        return
    
    conn.commit()
    conn.close()
    
    print()
    print("{}")

if __name__=="__main__":
    register()