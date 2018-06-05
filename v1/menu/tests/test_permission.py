#!/usr/bin/env python
# encoding: utf-8

from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from v1.menu.permissions import IsMenuOwner, IsMenuItemOwner
from v1.menu.models import MenuItem, Menu


class PermissionTest(TestCase):
    fixtures = [
        'test/users.json',
        'course_data.json',
        'cuisine_data.json',
        'recipe_data.json',
        'ing_data.json'
    ]

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
        self.menu = Menu.objects.create(title='food', author=self.user)
        self.item = MenuItem.objects.create(menu=self.menu, recipe_id=1)

    def test_is_list_owner_or_read_only(self):
        # Try and access something as an admin user.
        # Both get and post should have access.
        request = self.factory.get('/admin')
        request.user = self.staff
        self.assertTrue(IsMenuOwner().has_object_permission(request, None, None))
        self.assertTrue(IsMenuOwner().has_object_permission(request, None, self.menu))
        request = self.factory.post('/admin')
        request.user = self.staff
        self.assertTrue(IsMenuOwner().has_object_permission(request, None, None))
        self.assertTrue(IsMenuOwner().has_object_permission(request, None, self.menu))

        # Try and access something as an user who created th lists.
        # Both get and post should have access.
        request = self.factory.get('/admin')
        request.user = self.user
        self.assertTrue(IsMenuOwner().has_object_permission(request, None, self.menu))
        request = self.factory.post('/admin')
        request.user = self.user
        self.assertTrue(IsMenuOwner().has_object_permission(request, None, self.menu))

        # Try and access something as an anonymous user.
        # Both get and post should not have access.
        request = self.factory.get('/admin')
        request.user = AnonymousUser()
        self.assertFalse(IsMenuOwner().has_object_permission(request, None, self.menu))
        request = self.factory.post('/admin')
        request.user = AnonymousUser()
        self.assertFalse(IsMenuOwner().has_object_permission(request, None, self.menu))

    def test_is_item_owner_or_read_only(self):
        # Try and access something as an admin user.
        # Both get and post should have access.
        request = self.factory.get('/admin')
        request.user = self.staff
        self.assertTrue(IsMenuItemOwner().has_object_permission(request, None, None))
        self.assertTrue(IsMenuItemOwner().has_object_permission(request, None, self.item))
        request = self.factory.post('/admin')
        request.user = self.staff
        self.assertTrue(IsMenuItemOwner().has_object_permission(request, None, None))
        self.assertTrue(IsMenuItemOwner().has_object_permission(request, None, self.item))

        # Try and access something as an user who created th lists.
        # Both get and post should have access.
        request = self.factory.get('/admin')
        request.user = self.user
        self.assertTrue(IsMenuItemOwner().has_object_permission(request, None, self.item))
        request = self.factory.post('/admin')
        request.user = self.user
        self.assertTrue(IsMenuItemOwner().has_object_permission(request, None, self.item))

        # Try and access something as an anonymous user.
        # Both get and post should not have access.
        request = self.factory.get('/admin')
        request.user = AnonymousUser()
        self.assertFalse(IsMenuItemOwner().has_object_permission(request, None, self.item))
        request = self.factory.post('/admin')
        request.user = AnonymousUser()
        self.assertFalse(IsMenuItemOwner().has_object_permission(request, None, self.item))
