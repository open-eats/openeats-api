#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter(schema_title='Grocery Lists')
router.register(r'lists', views.GroceryListViewSet, base_name='GroceryList')
router.register(r'items', views.GroceryItemViewSet, base_name='GroceryItem')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^bulk_item/$', views.BulkGroceryItemViewSet.as_view()),
]
