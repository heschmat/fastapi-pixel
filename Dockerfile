FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential libffi-dev python3-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
