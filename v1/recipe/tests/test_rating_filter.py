#!/usr/bin/env python
# encoding: utf-8

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from v1.rating.average_rating import average_rating
from v1.recipe import views
from v1.recipe.models import Recipe


class RatingFilterTests(TestCase):
    """The rating filter has to work together with sorting and searching."""
    fixtures = [
        'test/users.json',
        'course_data.json',
        'cuisine_data.json',
        'ing_data.json',
        'recipe_data.json'
    ]

    def setUp(self):
        self.factory = APIRequestFactory()

    def get(self, query):
        view = views.RecipeViewSet.as_view({'get': 'list'}, throttle_classes=())
        request = self.factory.get('/api/v1/recipe/recipes/?' + query)
        request.user = AnonymousUser()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        return response.data

    def expected_ids(self, rating):
        return {
            r.id for r in Recipe.objects.filter(public=True)
            if average_rating(r.id) == rating
        }

    def test_rating_alone(self):
        data = self.get('rating=0&limit=100')
        self.assertTrue(data['results'])
        self.assertEqual({r['id'] for r in data['results']}, self.expected_ids(0))

    def test_rating_with_each_ordering(self):
        for ordering in ('title', '-title', 'pub_date', '-pub_date'):
            data = self.get('rating=0&limit=100&ordering=' + ordering)
            self.assertEqual({r['id'] for r in data['results']}, self.expected_ids(0), ordering)
            field = ordering.lstrip('-')
            wanted = list(Recipe.objects.filter(id__in=self.expected_ids(0))
                          .order_by(ordering).values_list(field, flat=True))
            got = [Recipe.objects.values_list(field, flat=True).get(id=r['id'])
                   for r in data['results']]
            self.assertEqual(got, wanted, ordering)
        for ordering in ('rating', '-rating'):
            data = self.get('rating=0&limit=100&ordering=' + ordering)
            self.assertEqual({r['id'] for r in data['results']}, self.expected_ids(0), ordering)

    def test_rating_with_search_and_filters(self):
        recipe = Recipe.objects.filter(public=True, id__in=self.expected_ids(0)).first()
        data = self.get('rating=0&search=%s&ordering=title' % recipe.title)
        self.assertIn(recipe.id, [r['id'] for r in data['results']])
        data = self.get('rating=0&course__slug=%s&ordering=title&limit=100' % recipe.course.slug)
        self.assertIn(recipe.id, [r['id'] for r in data['results']])
        self.assertEqual(self.get('rating=0&search=zzzznotarecipe')['count'], 0)

    def test_rating_hides_private_recipes_from_visitors(self):
        recipe = Recipe.objects.filter(id__in=self.expected_ids(0)).first()
        Recipe.objects.filter(id=recipe.id).update(public=False)
        data = self.get('rating=0&ordering=title&limit=100')
        self.assertNotIn(recipe.id, [r['id'] for r in data['results']])
