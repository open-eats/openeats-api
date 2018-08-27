#!/usr/bin/env python
# encoding: utf-8

from django.contrib import admin
from .models import MenuItem


class MenuItemAdmin(admin.ModelAdmin):
    # ordering = ['title', 'recipe']
    # list_display = ['recipe', 'title']
    # list_filter = ['recipe__title']
    # search_fields = ['title', 'recipe__title', ]
    pass


admin.site.register(MenuItem, MenuItemAdmin)
