#!/usr/bin/env sh

pip install coveralls==1.3.0
curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
chmod +x ./cc-test-reporter
./cc-test-reporter before-build

python manage.py reset_db --noinput
python manage.py migrate
coverage run manage.py test -k

./cc-test-reporter after-build --exit-code $TRAVIS_TEST_RESULT