FROM python:3.9
WORKDIR /home/app

COPY ./requirements.txt /home/app/

RUN apt update -qq
RUN pip install -r requirements.txt