FROM python:latest

WORKDIR /app

COPY . /app

RUN pip3 install pip setuptools mysql-connector-python blinker simplejson python-dotenv watchdog flask --upgrade

EXPOSE 80

CMD ["python","__init__.py"]