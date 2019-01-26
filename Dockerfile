FROM python

WORKDIR /code

RUN apt-get update && apt-get -y install texlive-full
RUN pip install cairocffi numpy
