#!/usr/bin/env python
# encoding: utf-8

from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from v1.recipe.models import Recipe
from v1.common.recipe_search import get_search_results
from v1.common.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class GetSearchResultsTests(TestCase):
    fixtures = [
        'test/users.json',
        'course_data.json',
        'cuisine_data.json',
        'ing_data.json',
        'recipe_data.json'
    ]

    def test_get_search_results(self):
        query = get_search_results(
            ['title', 'ingredient_groups__ingredients__title', 'tags__title'],
            Recipe.objects,
            'chili'
        ).distinct()

        self.assertTrue(len(query.all()) > 0)

    def test_get_search_no_results(self):
        query = get_search_results(
            ['title', 'ingredient_groups__ingredients__title', 'tags__title'],
            Recipe.objects,
            'blue berry'
        ).distinct()

        self.assertTrue(len(query.all()) == 0)


class PermissionTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret', is_staff=True
        )

    def test_is_owner_admin(self):
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request = self.factory.get('/admin')
        request.user = self.user
        self.assertTrue(
            IsOwnerOrReadOnly().has_permission(request, None)
        )
        request = self.factory.post('/admin')
        request.user = self.user
        self.assertTrue(
            IsOwnerOrReadOnly().has_permission(request, None)
        )

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        request = self.factory.get('/admin')
        request.user = AnonymousUser()
        self.assertTrue(
            IsOwnerOrReadOnly().has_permission(request, None)
        )
        request = self.factory.post('/admin')
        request.user = AnonymousUser()
        self.assertFalse(
            IsOwnerOrReadOnly().has_permission(request, None)
        )

    def test_is_admin_admin(self):
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
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

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
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
