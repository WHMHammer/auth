#!/usr/bin/python3
import whl    # a customized script
from json import dumps

@whl.debug
def request_reset_password():
    print("Content-Type: application/json")
    
    whl.check_request_method("POST")
    form=whl.get_form()
    
    try:
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
    
    if len(email)>whl.EMAILMAXLENGTH:
        print("Status: 400")
        print()
        print("{}")
        return
    
    conn=whl.connectDB()
    cur=conn.cursor()
    
    cur.execute("select username from users where email=%s limit 1;",(email,))
    try:
        username=cur.fetchone()[0]
    except TypeError:
        conn.close()
    else:
        challenge=whl.generate_salt()
        
        cur.execute("update users set challenge=%s where email=%s",(challenge,email))
        
        conn.commit()
        conn.close()
        
        reset_password_url="https://%s/auth/reset_password.html"%(whl.DOMAIN)
        whl.send_email(whl.NOREPLY,email,"Reset your password at %s"%whl.PROJECTNAME,"<p>Hello, dear %s:</p><p>Your verification code is:</p><p><code>%s</code></p>Please click <a href=\"%s\">here</a> or paste the following url to your web browser to continue reseting your password:</p><p>%s</p><br/><p>Best regards,</p><p>%s</p>"%(username,challenge,reset_password_url,reset_password_url,whl.PROJECTNAME))
    
    print()
    print("{}")

if __name__=="__main__":
    request_reset_password()