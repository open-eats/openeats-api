#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'mini-browse', views.MiniBrowseViewSet)
router.register(r'recipes', views.RecipeViewSet, basename='recipes')

urlpatterns = [
    url('', include(router.urls)),
]
