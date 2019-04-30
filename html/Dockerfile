FROM python:latest

EXPOSE 80

RUN pip3 install pip setuptools mysql-connector-python blinker simplejson python-dotenv watchdog flask --upgrade

WORKDIR /app

COPY . /app

CMD ["python","__init__.py"]