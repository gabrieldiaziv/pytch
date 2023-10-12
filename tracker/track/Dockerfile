FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt -y update &&  \ 
  apt -y install software-properties-common && \
  add-apt-repository -y ppa:deadsnakes/ppa && \
  apt -y install python3.9 python3.9-venv

WORKDIR /prototype

RUN python3.9 -m venv .venv && \
  .venv/bin/pip install jupyter 

COPY ./players.ipynb ./players.ipynb
