FROM python:3.12

WORKDIR /app/backend

COPY ../../../backend /app

# RUN chmod +x /app/deploy/docker/backend/server-entrypoint.sh
# RUN chmod +x /app/deploy/docker/backend/celery-entrypoint.sh

ARG CELERY_BROKER_URL
ARG CELERY_RESULT_BACKEND
ARG DJANGO_DB
ARG POSTGRES_HOST
ARG POSTGRES_PORT
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_NAME

RUN pip install --upgrade pip
RUN pip install -r /app/backend/requirements.txt
RUN python3 manage.py migrate
