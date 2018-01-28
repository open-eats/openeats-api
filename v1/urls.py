#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.conf.urls import include, url

urlpatterns = [
    url(r'^accounts/', include('v1.accounts.urls')),
    url(r'^recipe_groups/', include('v1.recipe_groups.urls')),
    url(r'^ingredient/', include('v1.ingredient.urls')),
    url(r'^list/', include('v1.list.urls')),
    url(r'^news/', include('v1.news.urls')),
    url(r'^recipe/', include('v1.recipe.urls')),
]
