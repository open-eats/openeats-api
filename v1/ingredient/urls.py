#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter(schema_title='Ingredients')
router.register(r'ingredient', views.IngredientViewSet)
router.register(r'ingredient-group', views.IngredientGroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
