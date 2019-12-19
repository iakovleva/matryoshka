FROM python:3

MAINTAINER Maxim Zelenkin <nudepatch@gmail.com>

RUN apt-get update -q && apt-get install -y \
    nano > /dev/null

RUN pip install scrapy

ENV APP_PATH /app
RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
