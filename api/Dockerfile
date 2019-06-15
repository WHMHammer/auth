FROM python:alpine

WORKDIR /app

EXPOSE 80

RUN pip3 install blinker simplejson python-dotenv watchdog flask
RUN pip3 install mysql-connector-python

COPY . /app

CMD ["python3", "__init__.py"]