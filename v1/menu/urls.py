#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'menu', views.MenuViewSet)
router.register(r'menu-item', views.MenuItemViewSet)

urlpatterns = [
    url('', include(router.urls)),
]
