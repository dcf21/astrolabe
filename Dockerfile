FROM python:3.14-bookworm

WORKDIR /code

RUN apt-get update && apt-get -y install texlive
RUN pip install cairocffi numpy scipy
