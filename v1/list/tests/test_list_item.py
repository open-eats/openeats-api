#!/usr/bin/env python
# encoding: utf-8

import json
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from v1.list import views
from v1.list.models import GroceryItem


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

    def test_list_bulk_delete(self):
        """Test to make sure the count is right for items after we delete"""
        view = views.BulkGroceryItemViewSet.as_view()
        request = self.factory.delete(
            '/api/v1/list/bulk_item',
            data=json.dumps([19, 20, 21]),
            content_type='application/json'
        )
        request.user = User.objects.get(pk=1)
        response = view(request)
        self.assertEqual(response.status_code, 204)

        self.assertEqual(len(GroceryItem.objects.filter(list_id=8)), 4)

        view = views.GroceryItemViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/list/items/?list=8')
        request.user = User.objects.get(pk=1)
        response = view(request)
        self.assertEqual(response.data.get('count'), 4)
