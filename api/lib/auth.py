import flask
from hashlib import sha3_512
from time import time

from info.auth import *
from lib import *


# check request entries (for database)
def check_username(username):
    return (
        bool(username) and
        len(username) <= username_max_length
    )


def check_salt(salt):
    return len(salt) == salt_length


def check_response(response):
    return len(response) == password_hash_length


def check_email(email):
    return len(email) <= email_max_length


def check_url(url):
    return len(url) <= url_max_length


# hash
def generate_salt():
    return rand_str(salt_length)


def hash(*args):
    if len(args) == 1:
        h = sha3_512(args[0])
        return h.hexdigest()
    s = args[-1]
    for i in range(len(args)-2, -1, -1):
        b = (args[i]+s).encode("utf8")
        h = sha3_512(b)
        s = h.hexdigest()
    return s


# user token
def generate_user_token(username):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, email, avatar
        FROM users
        WHERE username = %s
        LIMIT 1;
    """, (username,))

    user_id, email, avatar = cur.fetchone()

    session = generate_salt()
    cur.execute("""
        INSERT into sessions
        VALUES(%s,%s,%s);
    """, (user_id, session, int(time())+session_expire_time))

    conn.commit()
    conn.close()

    return {
        "user_id": user_id,
        "session": session,
        "username": username,
        "email": email,
        "avatar": avatar
    }


def check_user_token():
    user_token = flask.request.get_json().get("user_token")
    try:
        user_id = int(user_token["user_id"])
        session = str(user_token["session"])
    except (KeyError, TypeError):
        return None

    if not check_salt(session):
        return None

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        DELETE from sessions
        WHERE expire_time < %s;
    """, (int(time()),))

    conn.commit()

    cur.execute("""
        SELECT users.username, users.email, users.role
        FROM users RIGHT JOIN sessions
        ON users.id=sessions.user_id
        WHERE users.id=%s AND users.status=%s AND sessions.session=%s
        LIMIT 1;
    """, (user_id, "verified", session))

    try:
        username, email, role = cur.fetchone()
    except TypeError:
        return None

    return {
        "id": user_id,
        "username": username,
        "email": email,
        "role": role
    }
