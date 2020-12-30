#!/bin/sh

set -e

if [ ! -f /files/is_initialized ]; then
	python manage.py migrate --noinput
	python manage.py collectstatic --noinput
	touch /files/is_initialized
fi

gunicorn app.wsgi -b 0.0.0.0:8000