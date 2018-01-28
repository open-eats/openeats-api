#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.contrib import admin
from .models import News


class NewsAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'frontpage', 'pub_date']

admin.site.register(News, NewsAdmin)
