# Auth

This document describes the API design of the authentication system, the source code of which is under path [`/api/`](https://github.com/WHMHammer/auth/tree/master/api).

## RESTful API design

URL         | Method    | Description
-           | -         | -
register    | POST      | [Register](#Register)
register    | PUT       | [Verify registration](#Verify\ registration)
login       | GET       | [Get the "challenge"](#Get\ the\ "challenge")
login       | POST      | [Log in](#Send\ the\ "response")
login       | DELETE    | [Log out](#Log\ out)
password    | GET       | [Request to reset password](#Request\ to\ reset\ the\ password)
password    | PUT       | [Reset password](#Set\ a\ new\ password)
user        | GET       | [Get username](#Get\ username)
user        | PUT       | [Update user information](#Update\ user\ information)
user        | DELETE    | [Delete user](#Delete\ user)

## Registeration

### Register

### Verify registration

## Log in/out

### Log in

#### Get the "challenge"

#### Send the "response"

### Log out

## Forget password/username

### Reset password

#### Request to reset the password

#### Set a new password

### Get username

## Modify user

### Update user information

### Delete user
