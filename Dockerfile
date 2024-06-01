FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /source
RUN mkdir ./temp
RUN mkdir ./app

RUN apt update -y
RUN apt upgrade -y
RUN apt-get install software-properties-common -y

RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt install python3.12 -y
RUN apt install python3.12-venv -y
RUN apt install python3-pip -y

RUN cd /source && python3.12 -m venv venv
COPY requirements.txt /source/temp/requirements.txt
RUN . /source/venv/bin/activate && pip install -r /source/temp/requirements.txt