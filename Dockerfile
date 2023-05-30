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

ADD . /app

RUN chmod +x sh_scripts/wait_for_it.sh
RUN chmod +x sh_scripts/install_odbc_debian.sh && ./sh_scripts/install_odbc_debian.sh

RUN pip install -r requirements.txt