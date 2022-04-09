FROM python:3.8-alpine
LABEL maintainer="garmoshka"

WORKDIR /tutors_assistant/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="${PATH}:/root/.poetry/bin"

RUN apk update && apk add postgresql-dev gcc python3-dev zlib-dev musl-dev jpeg-dev libffi-dev g++
RUN pip install --upgrade pip
COPY poetry.lock pyproject.toml /tutors_assistant/
RUN pip install poetry && poetry install --no-interaction --no-ansi


COPY . /tutors_assistant/
