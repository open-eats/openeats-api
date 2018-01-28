#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.test import APIRequestFactory
from v1.list import views


class ListTests(TestCase):
    fixtures = ['test/users.json', 'test/lists.json', 'test/list_items.json']

    def setUp(self):
        self.factory = APIRequestFactory()

    def getResponse(self, user=None):
        view = views.GroceryListViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/list/lists/')
        if user:
            request.user = user
        return view(request)

    def test_get_lists(self):
        """Check if we get the right data for a list"""
        response = self.getResponse(User.objects.get(pk=1))

        self.assertEqual(response.data.get('count'), 2)

        results = response.data.get('results')
        totals = {"test-list": 7, "another-test-list": 5}

        for item in results:
            self.assertEquals(totals[item.get('slug')], item.get('item_count'))

    def test_anonymous_user_get_lists(self):
        """Check to make sure anonymous users don't get any data back"""
        response = self.getResponse(User.objects.get(pk=2))
        results = response.data.get('results')

        self.assertEquals(results, [])

    def test_no_lists_user_get_lists(self):
        """Make sure users with no lists get nothing back"""
        response = self.getResponse(AnonymousUser())
        results = response.data.get('results')

        self.assertEquals(results, [])
