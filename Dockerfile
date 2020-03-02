# cascade_app
FROM python:3.8-slim

# https://stackoverflow.com/a/54763270
ARG ENV

ENV ENV=${ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.3

# System deps:
RUN update-ca-certificates
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /application
COPY poetry.lock pyproject.toml /application/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /application
