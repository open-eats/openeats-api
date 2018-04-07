#!/usr/bin/env python
# encoding: utf-8

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from v1.recipe import views


class RecipeSerializerTests(TestCase):
    fixtures = [
        'test/users.json',
        'course_data.json',
        'cuisine_data.json',
        'ing_data.json',
        'recipe_data.json'
    ]

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_view_limiter(self):
        """Test to make sure we have the right fields"""
        view = views.RecipeViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe/recipes/tasty-chili?fields=id')
        response = view(request)

        self.assertTrue(response.data.get('id', True))
        self.assertFalse(response.data.get('title', False))

        view = views.RecipeViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe/recipes/tasty-chili?fields=id,title,photo')
        response = view(request)

        self.assertTrue(response.data.get('id', True))
        self.assertTrue(response.data.get('title', True))
        self.assertTrue(response.data.get('photo', True))
        self.assertFalse(response.data.get('directions', False))
        self.assertFalse(response.data.get('author', False))
