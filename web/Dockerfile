FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app
