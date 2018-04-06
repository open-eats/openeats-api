#!/usr/bin/env python
# encoding: utf-8

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from v1.recipe import views


class RecipeSerializerTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_simple_create_recipe(self):
        """Test to make sure we have the right fields"""
        view = views.RecipeViewSet.as_view({'post': 'create'})
        request = self.factory.get('/api/v1/recipe/recipes/')
        request.data = {
            "id": 1,
            "ingredients": [],
            "directions": '',
            "tags": [],
            "title": "Recipe name",
            "info": "Recipe info",
            "source": "",
            "prep_time": 60,
            "cook_time": 60,
            "servings": 8,
            "rating": 0,
            "author": 1,
            "cuisine": 1,
            "course": 2
        }
        response = view(request)

        self.assertTrue(response.data.get('id', True))
