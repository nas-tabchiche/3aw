# syntax=docker/dockerfile:1
# Based on https://docs.docker.com/samples/django/

FROM python:3.11
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install

COPY ./* /code/

ENTRYPOINT ["poetry", "run", "python", "manage.py", "runserver"]
EXPOSE 8000
