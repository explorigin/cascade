# cascade_app
FROM python:3.8-slim

# https://stackoverflow.com/a/54763270
ARG API_ENV

ENV API_ENV=${API_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.9 \
  POETRY_VIRTUALENVS_CREATE=false

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /application
COPY poetry.lock pyproject.toml /application/

# Project initialization:
RUN poetry install $(if [ "$API_ENV" = 'production' ]; then echo '--no-dev'; fi) --no-interaction --no-ansi \
  && if [ "$API_ENV" = 'production' ]; then rm -rf "$POETRY_CACHE_DIR"; fi \
  && poetry --version

# Creating folders, and files for a project:
COPY . /application
