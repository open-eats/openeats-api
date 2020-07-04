#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from v1.recipe_groups import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'cuisine-count', views.CuisineCountViewSet, basename='cuisine-count')
router.register(r'cuisine', views.CuisineViewSet, basename='cuisine')
router.register(r'course-count', views.CourseCountViewSet, basename='course-count')
router.register(r'course', views.CourseViewSet, basename='course')
router.register(r'tag', views.TagViewSet)

urlpatterns = [
    url('', include(router.urls)),
]
