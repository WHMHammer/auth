# Documenmtation for login API

## Introduction

This documentation explains how to log into an account. The API is based on HTTP. "Chellenge-response authentication" is used so 2 requests need to be sent.

## Challenge

The 1st request is to get the "salt" and "challenge" of the account.

### Request

The request should be sent to [https://devpsu.whmhammer.com/cgi/challenge.py](https://devpsu.whmhammer.com/cgi/challenge.py) using **POST** method with the following parameter:

### `login` (REQUIRED)

The username **or** the email address of the account.

### Response

The response is always in `application/json`.

- `status`: the status of the request for a challenge. Here is a list of all possible values (case sensitive):

    - `success`

    - `use POST method`

    - `missing parameter`

    - `illegal login`

    - `user not found`

    - `user hasn't been verified`

    - `unexpected error`

- `challenge`: a randomly generated "challenge". The challenge is also a 32-digit string containing only alphabetical and digital characters. The "challenge" is in the same format as the "salt" but they function differently.

- `salt` : the "salt" generated during registration.

A new challenge is written to the database only when `status` is `success`.

## Response

The 2nd request sends the hashed password to the server.

### Request

The request should be sent to [https://devpsu.whmhammer.com/cgi/login.py](https://devpsu.whmhammer.com/cgi/login.py) using **POST** method with the following parameter:

#### `login` (REQUIRED)

The username **or** the email address of the account.

#### `response` (REQUIRED)

The 128-digit **hexadecimal digestion** of the **sha512** hash of the concatenation of the "challenge" (got from the previous request) and the 128-digit **hexadecimal digestion** of the **sha512** hash of the concatenation of the "salt" (got from the previous request) and the raw password.

### Response

The response is always in `application/json`.

- `status`: the status of the login attempt. Here is a list of all possible values (case sensitive):

    - `success`

    - `use POST method`

    - `missing parameter`

    - `illegal login` (the `login` given is neither a legal username nor a legal email address)

    - `use sha512`

    - `user not found`

    - `user hasn't been verified`

    - `fail` (the `response` given does not match the hashed password in database)

    - `unexpected error`

The user is successfully logged into the account only when `status` is `success`.

## Sample front-end implementation

### Python3

<pre><code>
import requests as rq
from hashlib import sha512

login="username"
#login="johndoe@e.mail"
password="password"

r=rq.post("https://devpsu.whmhammer.com/cgi/challenge.py",{"login":login})

print(r.json())

salt=r.json().get("salt")
challenge=r.json().get("challenge")

b=bytes(salt+password,"ascii")
h=sha512(b)
b=bytes(challenge+h.hexdigest(),"ascii")
h=sha512(b)

data={
    "login":login,
    "response":h.hexdigest()
}

r=rq.post("https://devpsu.whmhammer.com/cgi/login.py",data)

print(r.json())
</code></pre>