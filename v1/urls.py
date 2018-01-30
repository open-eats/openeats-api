#!/usr/bin/env python
# encoding: utf-8

from django.urls import include, path

app_name='v1'
urlpatterns = [
    path('accounts/', include('v1.accounts.urls')),
    path('recipe_groups/', include('v1.recipe_groups.urls')),
    path('ingredient/', include('v1.ingredient.urls')),
    path('list/', include('v1.list.urls')),
    path('news/', include('v1.news.urls')),
    path('recipe/', include('v1.recipe.urls')),
]
