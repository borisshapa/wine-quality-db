FROM python:3.10-slim

ARG USER_ID
ARG PASSWORD
ARG SERVER

ENV USER_ID=${USER_ID}
ENV PASSWORD=${PASSWORD}
ENV SERVER=${SERVER}

RUN apt-get update && apt-get -y install curl gnupg2

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app

COPY install_odbc_debian.sh /app

RUN chmod u+x install_odbc_debian.sh && ./install_odbc_debian.sh

ADD . /app

RUN pip install -r requirements.txt
