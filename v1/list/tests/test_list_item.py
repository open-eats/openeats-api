#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.test import APIRequestFactory
from v1.list import views


class ListTests(TestCase):
    fixtures = ['test/users.json', 'test/lists.json', 'test/list_items.json']

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_list_item_count(self):
        """Test to make sure the count is right for items"""
        view = views.GroceryItemViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/list/items/?list=8')
        request.user = User.objects.get(pk=1)
        response = view(request)

        self.assertEqual(response.data.get('count'), 7)
