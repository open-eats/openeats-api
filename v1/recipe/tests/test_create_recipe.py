#!/usr/bin/env python
# encoding: utf-8

import os
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from rest_framework.test import APIRequestFactory
from v1.recipe import views


class RecipeSerializerTests(TestCase):
    fixtures = [
        'test/users.json',
        'course_data.json',
        'cuisine_data.json',
    ]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.staff = User.objects.create_user(
            username='staff', email='staff@gmail.com', password='top_secret', is_superuser=True
        )

    def test_simple_create_recipe(self):
        """Test to make sure we have the right fields"""
        view = views.RecipeViewSet.as_view({'post': 'create'})
        data = {
            "ingredient_groups": [
                {
                    "id": 3,
                    "title": "",
                    "ingredients": []
                },
                {
                    "id": 4,
                    "title": "Veges",
                    "ingredients": [
                        {
                            "id": 13,
                            "numerator": 1.0,
                            "denominator": 2.0,
                            "measurement": "dash",
                            "title": "black pepper"
                        },
                        {
                            "id": 14,
                            "numerator": 4.0,
                            "denominator": 1.0,
                            "measurement": "tablespoons",
                            "title": "chili powder"
                        },
                        {
                            "id": 15,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "tablespoon",
                            "title": "cumin"
                        },
                        {
                            "id": 16,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "can",
                            "title": "dark kidney beans"
                        },
                        {
                            "id": 17,
                            "numerator": 2.0,
                            "denominator": 1.0,
                            "measurement": "cans",
                            "title": "diced tomatos"
                        },
                        {
                            "id": 18,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "whole",
                            "title": "green bell pepper"
                        },
                        {
                            "id": 19,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "can",
                            "title": "light kidney beans"
                        },
                        {
                            "id": 20,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "whole",
                            "title": "serrano pepper"
                        },
                        {
                            "id": 21,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "whole",
                            "title": "white onion"
                        }
                    ]
                },
                {
                    "id": 5,
                    "title": "Beef",
                    "ingredients": [
                        {
                            "id": 22,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "pound",
                            "title": "ground pork"
                        },
                        {
                            "id": 23,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "pound",
                            "title": "ground sirloin"
                        },
                        {
                            "id": 24,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "dash",
                            "title": "kosher salt"
                        }
                    ]
                }
            ],
            "directions": '',
            "tags": ['hi', 'hello'],
            "title": "Recipe name",
            "info": "Recipe info",
            "source": "google.com",
            "prep_time": 60,
            "cook_time": 60,
            "servings": 8,
            "rating": 0,
            "cuisine": 1,
            "course": 2
        }
        request = self.factory.post('/api/v1/recipe/recipes/', data=data)
        request.user = self.staff

        root_path = os.path.join(settings.PROJECT_PATH, 'v1', 'fixtures', 'test', 'food.jpg')
        with open(root_path, 'rb') as f:
            request.FILES['photo'] = SimpleUploadedFile(
                root_path,
                f.read(),
                content_type='multipart/form-data'
            )
        response = view(request)

        self.assertTrue(response.data.get('id', True))
