#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
from copy import deepcopy
import unittest
import mock

from django.test import TestCase
from v1.recipe.serializers import RecipeSerializer
from v1.recipe.models import Recipe


class RecipeSerializerTests(unittest.TestCase):
    def setUp(self):
        self.serializer = RecipeSerializer()
        self.data = {
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

    def test_rating_over_success(self):
        data = deepcopy(self.data)

        data['rating'] = 20

        recipe = mock.Mock(spec=Recipe)
        response = self.serializer.update(recipe, data)

        self.assertEqual(response.rating, 5)

    def test_rating_under_success(self):
        data = deepcopy(self.data)

        data['rating'] = -20

        recipe = mock.Mock(spec=Recipe)
        response = self.serializer.update(recipe, data)

        self.assertEqual(response.rating, 0)

    def test_no_rating_supplied_success(self):
        data = deepcopy(self.data)

        del data['rating']

        recipe = mock.Mock(spec=Recipe)
        recipe.rating = 3
        response = self.serializer.update(recipe, data)

        self.assertEqual(response.rating, 3)

