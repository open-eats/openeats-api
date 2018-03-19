#!/usr/bin/env sh

pip install coveralls==1.3.0

python manage.py reset_db --noinput
python manage.py migrate
coverage run manage.py test -k
coveralls
