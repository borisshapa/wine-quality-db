FROM python:3.10-slim

RUN apt-get update && apt-get -y install curl gnupg2

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app

COPY install_odbc_debian.sh /app

RUN chmod u+x install_odbc_debian.sh && ./install_odbc_debian.sh

ADD . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["bash"]
