# OpenEats API

[![API Build Status](https://travis-ci.org/open-eats/openeats-api.svg?branch=master)](https://travis-ci.org/open-eats/openeats-api)
[![Coverage Status](https://coveralls.io/repos/github/open-eats/openeats-api/badge.svg)](https://coveralls.io/github/open-eats/openeats-api)
[![Maintainability](https://api.codeclimate.com/v1/badges/ac4a42717db53286ee8f/maintainability)](https://codeclimate.com/github/open-eats/openeats-api/maintainability)

This is the API that powers OpenEats. It uses Django/Django Rest Framework to power the API. The core responsibilities of the APi are:
- OpenEats REST API
- Django User management with Django REST token auth
- Django Admin panel for creating new users and administration
- Static Media Manangemtn (AKA Recipe Images)

See [the homepage](https://github.com/open-eats/OpenEats) for more information about OpenEats!

# Contributing
Please read the [contribution guidelines](https://github.com/open-eats/openeats-api/blob/master/CONTRIBUTING.md) in order to make the contribution process easy and effective for everyone involved.

# Dev Tips

#### Running tests
To run tests locally:

```bash
cd openeats-web
docker-compose -f test.yml -p test build
docker-compose -f test.yml -p test up -d db
docker-compose -f test.yml -p test run --rm --entrypoint sh api
python manage.py test
```

Note: If this is the first time you are running the tests, give the DB some time to build itself once it's build there is no need to wait again.

#### REST Endpoints
You can access the API roots via there app names:
* Recipes - http://localhost:8000/api/v1/recipe
* Ingredients - http://localhost:8000/api/v1/ingredient/
* Recipe groups - http://localhost:8000/api/v1/recipe_groups/
* News - http://localhost:8000/api/v1/news/
* Lists - http://localhost:8000/api/v1/list/