FROM python:3.12

WORKDIR /app

COPY . /app

RUN chmod +x server-entrypoint.sh
RUN chmod +x celery-entrypoint.sh

ARG CELERY_BROKER_URL
ARG CELERY_RESULT_BACKEND
ARG DJANGO_DB
ARG POSTGRES_HOST
ARG POSTGRES_PORT
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_NAME

RUN pip install --upgrade pip
RUN pip install -r ./backend/requirements.txt
RUN python3 ./backend/manage.py migrate
