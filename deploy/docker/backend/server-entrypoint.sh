#!/bin/sh

until cd /app/backend; do
	echo "Waiting for backend volume..."
done

until python3 manage.py migrate; do
	echo "Waiting for db to be ready..."
	sleep 2
done

daphne backend.asgi:application --bind 0.0.0.0 --port 8000
