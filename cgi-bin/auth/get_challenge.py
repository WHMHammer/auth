#!/usr/bin/python3
import whl    # a customized script
from json import dumps

@whl.debug
def get_challenge():
    print("Content-Type: application/json")
    
    whl.check_request_method("POST")
    form=whl.get_form()
    
    try:
        username=form["username"]
    except KeyError:
        print("Status: 400")
        print()
        print("{}")
        return
    
    if len(username)>whl.USERNAMEMAXLENGTH:
        print("Status: 400")
        print()
        print("{}")
        return
    
    conn=whl.connectDB()
    cur=conn.cursor()
    
    cur.execute("select salt from users where username=%s and status=%s;",(username,"verified"))
    try:
        salt=cur.fetchone()[0]
    except TypeError:
        conn.close()
        print("Status: 404")
        print()
        print("{}")
        return
    
    challenge=whl.generate_salt()
    
    cur.execute("update users set challenge=%s where username=%s;",(challenge,username))
    
    conn.commit()
    conn.close()
    
    print()
    print(dumps({
        "salt":salt,
        "challenge":challenge
    }))

if __name__=="__main__":
    get_challenge()