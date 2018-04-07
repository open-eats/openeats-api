#!/usr/bin/env python
# encoding: utf-8

from django.test import TestCase
from v1.recipe.models import Recipe
from v1.common.recipe_search import get_search_results


class GetSearchResultsTests(TestCase):
    fixtures = [
        'test/users.json',
        'course_data.json',
        'cuisine_data.json',
        'recipe_data.json'
        'ing_data.json',
    ]

    def test_get_search_results(self):
        """ Run a search that will return data """
        query = get_search_results(
            ['title', 'ingredient_groups__ingredients__title', 'tags__title'],
            Recipe.objects,
            'chili'
        ).distinct()

        self.assertTrue(len(query.all()) > 0)

    def test_get_search_no_results(self):
        """ Run a search that will return no data """
        query = get_search_results(
            ['title', 'ingredient_groups__ingredients__title', 'tags__title'],
            Recipe.objects,
            'blue berry'
        ).distinct()

        self.assertTrue(len(query.all()) == 0)
