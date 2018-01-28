#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter(schema_title='Recipes')
router.register(r'mini-browse', views.MiniBrowseViewSet)
router.register(r'recipes', views.RecipeViewSet, base_name='recipes')
router.register(r'rating', views.RatingViewSet, base_name='rating')

urlpatterns = [
    url(r'^', include(router.urls)),
]
