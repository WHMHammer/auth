# Auth (challenge-response)

This project aims to provide a secure web based authentication system.

## To-Do

Planned:

- Documentation
  
Please create an issue if you feel that new features need to be added.

## Deploy

- Download the source code to your server.

- Create a database with `schema.sql`.

- Change the values of critical variables in `api/auth/__init__.py` and `html/static/js/info.js`.

- `cd` to the source code directory.

### Docker (recommended)

```
docker build -t [api image name] api
docker build -t [html image name] html
docker run -p [ip address]:[port number]:80 -d [api image name]
docker run -p [ip address]:[port number]:80 -d [html image name]
```
e.g.

```
docker build -t auth_api api
docker build -t auth_html html
docker run -p 127.0.0.11:8080:80 -d auth_api
docker run -p 127.0.0.10:8080:80 -d auth_html
```

You can then expose your containers to the Internet by using [reverse proxy](http://flask.pocoo.org/docs/1.0/deploying/wsgi-standalone/#proxy-setups).

### Others

Read [flask](https://github.com/pallets/flask)'s [official document on deployment](http://flask.pocoo.org/docs/1.0/tutorial/deploy/?highlight=deploy) for other ways to deploy the project.

## Documentation

(not yet available)

## Acknowledgements

### [**Staph. aureus**](https://github.com/StephDC)

Special thanks to [Staph. aureus](https://github.com/StephDC) for leading me the way to web development, and being a real good friend in my life. I wouldn't be able to accompllish this without your guidance.

### [Brian Turek](https://github.com/Caligatio) - [jsSHA](https://github.com/Caligatio/jsSHA)
