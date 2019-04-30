# Auth

This project aims to provide a secure web based authentication system. The project runs in `docker` containers with `flask`.

## Status

This project is still under construction.

## Dependency

`docker-ce`

## Deploy

Change to the project directory, run the following command:

`docker build -t your_image_tag .`

Docker will automatically download other dependencies required.

After building the docker image, run this:

`docker run --name your_instance_name your_image_tag`

You can also add `-d` tag in order to run it in the background.

(to be continued)

## Documentation

See `/doc` directory.