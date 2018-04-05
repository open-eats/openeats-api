#!/usr/bin/env python
# encoding: utf-8

from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from v1.common.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class PermissionTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        # Create a staff user.
        self.user = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret', is_staff=True
        )

    def test_is_owner_or_read_only(self):
        # Try and access something as an admin user.
        # Both get and post should have access.
        request = self.factory.get('/admin')
        request.user = self.user
        self.assertTrue(
            IsOwnerOrReadOnly().has_permission(request, None)
        )
        self.assertTrue(
            IsOwnerOrReadOnly().has_object_permission(request, None, None)
        )
        request = self.factory.post('/admin')
        request.user = self.user
        self.assertTrue(
            IsOwnerOrReadOnly().has_permission(request, None)
        )

        # Try and access something as an anonymous user.
        # Both get should have access but post shouldn't.
        request = self.factory.get('/admin')
        request.user = AnonymousUser()
        self.assertTrue(
            IsOwnerOrReadOnly().has_permission(request, None)
        )
        self.assertTrue(
            IsOwnerOrReadOnly().has_object_permission(request, None, None)
        )
        request = self.factory.post('/admin')
        request.user = AnonymousUser()
        self.assertFalse(
            IsOwnerOrReadOnly().has_permission(request, None)
        )

    def test_is_admin_or_read_only(self):
        # Try and access something as an admin user.
        # Both get and post should have access.
        request = self.factory.get('/admin')
        request.user = self.user
        self.assertTrue(
            IsAdminOrReadOnly().has_permission(request, None)
        )
        request = self.factory.post('/admin')
        request.user = self.user
        self.assertTrue(
            IsAdminOrReadOnly().has_permission(request, None)
        )

        # Try and access something as an anonymous user.
        # Both get should have access but post shouldn't.
        request = self.factory.get('/admin')
        request.user = AnonymousUser()
        self.assertTrue(
            IsAdminOrReadOnly().has_permission(request, None)
        )
        request = self.factory.post('/admin')
        request.user = AnonymousUser()
        self.assertFalse(
            IsAdminOrReadOnly().has_permission(request, None)
        )
