#!/usr/bin/env python
# encoding: utf-8

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'lists', views.GroceryListViewSet, basename='GroceryList')
router.register(r'items', views.GroceryItemViewSet, basename='GroceryItem')

urlpatterns = [
    path('', include(router.urls)),
    path('bulk_item/', views.BulkGroceryItemViewSet.as_view()),
]
