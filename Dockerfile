FROM python:3.6.4

WORKDIR /src

ADD requirements.txt /src/requirements.txt
RUN pip3 install -r /src/requirements.txt

ADD . /src
