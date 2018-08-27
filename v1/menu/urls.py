#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'menu', views.MenuViewSet)
router.register(r'menu-item', views.MenuItemViewSet)
router.register(r'menu-recipes', views.RecipeItemViewSet)

urlpatterns = [
    url('', include(router.urls)),
    url(r'^menu-copy/$', views.MenuCopyViewSet.as_view())
]
