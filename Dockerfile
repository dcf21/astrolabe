FROM python:3.6-buster

WORKDIR /code

RUN apt-get update && apt-get -y install texlive
RUN pip install cairocffi numpy scipy
