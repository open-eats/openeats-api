#!/usr/bin/env python
# encoding: utf-8

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'menu-item', views.MenuItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'menu-stats/',
        views.MenuStatsViewSet.as_view(),
        name='menu_stats'
    ),
]
