#!/bin/sh

until cd /app/backend; do
	echo "Waiting for backend volume..."
done

celery -A backend worker -l info
