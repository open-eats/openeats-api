#!/usr/bin/env python
# encoding: utf-8

from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from v1.list.permissions import IsListOwner, IsItemOwner
from v1.list.models import GroceryList, GroceryItem


class PermissionTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        # Create a staff user.
        self.staff = User.objects.create_user(
            username='staff', email='staff@gmail.com', password='top_secret', is_superuser=True
        )
        self.user = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret'
        )
        self.list = GroceryList.objects.create(title='food', author=self.user)
        self.item = GroceryItem.objects.create(title='bacon', list=self.list)

    def test_is_list_owner_or_read_only(self):
        # Try and access something as an admin user.
        # Both get and post should have access.
        request = self.factory.get('/admin')
        request.user = self.staff
        self.assertTrue(IsListOwner().has_object_permission(request, None, None))
        self.assertTrue(IsListOwner().has_object_permission(request, None, self.list))
        request = self.factory.post('/admin')
        request.user = self.staff
        self.assertTrue(IsListOwner().has_object_permission(request, None, None))
        self.assertTrue(IsListOwner().has_object_permission(request, None, self.list))

        # Try and access something as an user who created th lists.
        # Both get and post should have access.
        request = self.factory.get('/admin')
        request.user = self.user
        self.assertTrue(IsListOwner().has_object_permission(request, None, self.list))
        request = self.factory.post('/admin')
        request.user = self.user
        self.assertTrue(IsListOwner().has_object_permission(request, None, self.list))

        # Try and access something as an anonymous user.
        # Both get and post should not have access.
        request = self.factory.get('/admin')
        request.user = AnonymousUser()
        self.assertFalse(IsListOwner().has_object_permission(request, None, self.list))
        request = self.factory.post('/admin')
        request.user = AnonymousUser()
        self.assertFalse(IsListOwner().has_object_permission(request, None, self.list))

    def test_is_item_owner_or_read_only(self):
        # Try and access something as an admin user.
        # Both get and post should have access.
        request = self.factory.get('/admin')
        request.user = self.staff
        self.assertTrue(IsItemOwner().has_object_permission(request, None, None))
        self.assertTrue(IsItemOwner().has_object_permission(request, None, self.item))
        request = self.factory.post('/admin')
        request.user = self.staff
        self.assertTrue(IsItemOwner().has_object_permission(request, None, None))
        self.assertTrue(IsItemOwner().has_object_permission(request, None, self.item))

        # Try and access something as an user who created th lists.
        # Both get and post should have access.
        request = self.factory.get('/admin')
        request.user = self.user
        self.assertTrue(IsItemOwner().has_object_permission(request, None, self.item))
        request = self.factory.post('/admin')
        request.user = self.user
        self.assertTrue(IsItemOwner().has_object_permission(request, None, self.item))

        # Try and access something as an anonymous user.
        # Both get and post should not have access.
        request = self.factory.get('/admin')
        request.user = AnonymousUser()
        self.assertFalse(IsItemOwner().has_object_permission(request, None, self.item))
        request = self.factory.post('/admin')
        request.user = AnonymousUser()
        self.assertFalse(IsItemOwner().has_object_permission(request, None, self.item))
