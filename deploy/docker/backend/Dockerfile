FROM python:3.12

WORKDIR /app/backend

COPY . /app

RUN chmod +x /app/deploy/docker/backend/server-entrypoint.sh
RUN chmod +x /app/deploy/docker/backend/celery-entrypoint.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 manage.py migrate
