# syntax=docker/dockerfile:1
FROM python:3.9-slim

WORKDIR /app

RUN pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml /app/

RUN poetry config virtualenvs.create false \
    && poetry install

COPY ./src /app/src
