#!/usr/bin/env python
# encoding: utf-8

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from v1.recipe_groups import views


class RecipeGroupsTests(TestCase):
    fixtures = [
        'test/users.json',
        'course_data.json',
        'cuisine_data.json',
        'recipe_data.json'
    ]

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_cuisine_all(self):
        view = views.CuisineCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/cuisine-count/')
        response = view(request)

        self.assertEqual(response.data.get('count'), 1)

        results = response.data.get('results')
        totals = {"american": 31}

        for item in results:
            self.assertEquals(totals[item.get('slug')], item.get('total'))

    def test_course_all(self):
        view = views.CourseCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/course-count/')
        response = view(request)

        self.assertEqual(response.data.get('count'), 1)

        results = response.data.get('results')
        totals = {"entry": 31}

        for item in results:
            self.assertEquals(totals[item.get('slug')], item.get('total'))

    def test_cuisine_with_filters(self):
        view = views.CuisineCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/cuisine-count/?course=entry&rating=3')
        response = view(request)

        self.assertEqual(response.data.get('count'), 1)

        results = response.data.get('results')
        totals = {"american": 31}

        for item in results:
            self.assertEquals(totals[item.get('slug')], item.get('total'))

    def test_cuisine_with_course_filter_no_results(self):
        view = views.CuisineCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/cuisine-count/?course=entry&rating=0')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)

    def test_cuisine_with_non_existent_course(self):
        view = views.CuisineCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/cuisine-count/?course=non-existent')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)

    def test_course_with_filters(self):
        view = views.CourseCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/course-count/?cuisine=american&rating=3')
        response = view(request)

        self.assertEqual(response.data.get('count'), 1)

        results = response.data.get('results')
        totals = {"entry": 31}

        for item in results:
            self.assertEquals(totals[item.get('slug')], item.get('total'))

    def test_course_with_cuisine_filter_no_results(self):
        view = views.CourseCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/course-count/?cuisine=american&rating=0')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)

    def test_course_with_non_existent_cuisine(self):
        view = views.CourseCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/course-count/?cuisine=non-existent')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)
