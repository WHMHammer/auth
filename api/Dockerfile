FROM python:latest

WORKDIR /app

EXPOSE 80

RUN pip3 install mysql-connector-python blinker simplejson python-dotenv watchdog flask

COPY . /app

CMD ["python3", "__init__.py"]