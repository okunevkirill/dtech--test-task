FROM python:3.10.7

RUN mkdir -p /usr/src/
WORKDIR /usr/src/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /usr/src/

COPY . /usr/src/

RUN poetry install --only main
