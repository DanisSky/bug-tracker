FROM python:3.9

WORKDIR /code/

ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.1.12
COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . /code