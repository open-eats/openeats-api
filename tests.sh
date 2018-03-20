#!/usr/bin/env sh

# Install test related dependencies
pip install coveralls==1.3.0
apk add git
apk add curl

# Install Code Climate script
curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
chmod +x ./cc-test-reporter
./cc-test-reporter before-build

# Prep the DB for testing
python manage.py reset_db --noinput
python manage.py migrate

# Run the tests and create a coverage report
coverage run --omit="*/migrations*,*/fixtures*" manage.py test -k

# Submit coverage to Coveralls
coveralls

# Submit report to Code Climate
./cc-test-reporter after-build --exit-code 0
