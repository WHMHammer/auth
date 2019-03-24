#!/usr/bin/python3
import whl    # a customized script
from json import dumps

@whl.debug
def get_username():
    print("Content-Type: application/json")
    
    whl.check_request_method("POST")
    
    form=whl.get_form()
    
    try:
        email=form["email"]
    except KeyError:
        print("Status: 400")
        print()
        print("{}")
        exit()
    
    if len(email)>whl.EMAILMAXLENGTH:
        print("Status: 400")
        print()
        print("{}")
        exit()
    
    conn=whl.sql.connect(whl.DBHOST,whl.DBUSER,whl.DBPASSWORD,whl.DBNAME)
    cur=conn.cursor()
    
    cur.execute("select username from users where email=%s and status=%s;",(email,"verified"))
    try:
        username=cur.fetchone()[0]
    except TypeError:
        pass
    else:
        whl.send_email(whl.NOREPLY,email,"Your username at %s"%whl.PROJECTNAME,"<p>Your username at %s is:</p><p>%s</p><br/><p>Best regards,</p><p>%s</p>"%(whl.PROJECTNAME,username,whl.PROJECTNAME))
    
    conn.close()
    
    print()
    print("{}")

if __name__=="__main__":
    get_username()