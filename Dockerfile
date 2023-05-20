FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /code
RUN apt update
RUN apt install -y --assume-yes python3-dev libpq-dev build-essential python3-pip
RUN apt-get install libgeos-dev -y


COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
