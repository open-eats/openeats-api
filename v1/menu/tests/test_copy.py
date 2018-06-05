#!/usr/bin/env python
# encoding: utf-8

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from v1.menu.models import MenuItem, Menu
from datetime import datetime

from v1.menu import views


class ListTests(TestCase):
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
        self.menu = Menu.objects.create(title='food', author=self.staff)
        self.item = MenuItem.objects.create(menu=self.menu, recipe_id=1)

    def test_get_copy_menu(self):
        """Check if we get the right data for a list"""
        view = views.MenuCopyViewSet.as_view()
        data = {
            'menu': '1',
            'title': 'new menu',
            'description': 'this is new',
            'start': datetime.now(),
        }
        request = self.factory.post('/api/v1/recipe/recipes/', data=data)
        request.user = self.staff
        response = view(request)

        print(response.data)

        self.assertTrue(response.data.get('id', True))
