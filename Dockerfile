FROM python:3.10.0-alpine

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /temp/requirements.txt
COPY . /code

EXPOSE 8000

WORKDIR /code

RUN pip install --upgrade pip
RUN apk add gcc musl libffi-dev
RUN pip install -r /temp/requirements.txt
RUN adduser --disabled-password service-user

USER service-user
