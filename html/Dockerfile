FROM python:latest

WORKDIR /app

EXPOSE 80

RUN pip3 install flask

COPY . /app

CMD ["python3", "__init__.py"]