# syntax=docker/dockerfile:1
FROM python:3.10.10-slim

ENV AIRFLOW_HOME=/app

WORKDIR /app

RUN apt update && apt install -y build-essential libpq-dev netcat

RUN pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install

# Copy the airflow.cfg file
COPY airflow.cfg /app/airflow.cfg

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh

#COPY ./src /app/src

# airflow webserver port
EXPOSE 8080

# Use the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]