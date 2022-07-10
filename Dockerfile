FROM python:3.10-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install pip==22.1.2
COPY . .
RUN pip install -r requirements.txt

