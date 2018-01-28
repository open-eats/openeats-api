#!/usr/bin/env sh

# Update the DB if it needs it and compile static files.
/code/manage.py migrate --no-input
/code/manage.py collectstatic --no-input

# Start up gunicorn
/code/base/gunicorn_start.sh
