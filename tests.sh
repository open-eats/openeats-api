#!/usr/bin/env sh

# Install test related dependencies
pip install coveralls==1.3.0
apk add git

# Prep the DB for testing
python manage.py reset_db --noinput
python manage.py migrate

# Run the tests and create a coverage report
coverage run --omit="*/migrations*,*/fixtures*" manage.py test -k
if [ $? -eq 0 ]
then
  echo "The script ran ok"
  exit 0
else
  echo "The script failed" >&2
  exit 1
fi

# Submit coverage to Coveralls
coveralls
