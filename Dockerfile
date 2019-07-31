FROM python:3.7
MAINTAINER Jan Okruta

ENV PYTHONUNBUFFERED 1

RUN mkdir /scraper
WORKDIR /scraper
COPY . /scraper

RUN pip install -r requirements.txt