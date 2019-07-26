FROM python

WORKDIR /app

EXPOSE 80

RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install uwsgi blinker simplejson python-dotenv watchdog flask
RUN pip3 install mysql-connector-python

COPY . /app

CMD uwsgi --http :80 --master --wsgi-file __init__.py --callable app