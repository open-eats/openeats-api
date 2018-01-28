#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from v1.recipe_groups import views


class RecipeGroupsTests(TestCase):
    fixtures = ['test/users.json', 'test/cuisine.json', 'test/course.json', 'test/recipes.json']

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_cuisine_all(self):
        view = views.CuisineCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/cuisine-count/')
        response = view(request)

        self.assertEqual(response.data.get('count'), 3)

        results = response.data.get('results')
        totals = {"cuisine-1": 3, "cuisine-2": 2, "cuisine-3": 1}

        for item in results:
            self.assertEquals(totals[item.get('slug')], item.get('total'))

    def test_course_all(self):
        view = views.CourseCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/course-count/')
        response = view(request)

        self.assertEqual(response.data.get('count'), 3)

        results = response.data.get('results')
        totals = {"course-1": 3, "course-2": 2, "course-3": 1}

        for item in results:
            self.assertEquals(totals[item.get('slug')], item.get('total'))

    def test_cuisine_with_filters(self):
        view = views.CuisineCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/cuisine-count/?course=course-1&rating=0')
        response = view(request)

        self.assertEqual(response.data.get('count'), 1)

        results = response.data.get('results')
        totals = {"cuisine-1": 1}

        for item in results:
            self.assertEquals(totals[item.get('slug')], item.get('total'))

    def test_cuisine_with_course_filter_no_results(self):
        view = views.CuisineCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/cuisine-count/?course=course-4&rating=0')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)

    def test_cuisine_with_non_existent_course(self):
        view = views.CuisineCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/cuisine-count/?course=non-existent')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)

    def test_course_with_filters(self):
        view = views.CourseCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/course-count/?cuisine=cuisine-1&rating=1')
        response = view(request)

        self.assertEqual(response.data.get('count'), 1)

        results = response.data.get('results')
        totals = {"course-3": 1}

        for item in results:
            self.assertEquals(totals[item.get('slug')], item.get('total'))

    def test_course_with_cuisine_filter_no_results(self):
        view = views.CourseCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/course-count/?cuisine=cuisine-4&rating=0')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)

    def test_course_with_non_existent_cuisine(self):
        view = views.CourseCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/course-count/?cuisine=non-existent')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)
