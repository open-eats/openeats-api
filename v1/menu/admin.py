#!/usr/bin/env python
# encoding: utf-8

from django.contrib import admin
from .models import Menu, MenuItem


class MenuAdmin(admin.ModelAdmin):
    # ordering = ['title', 'ingredient_group']
    # list_display = ['title', 'quantity', 'measurement']
    # list_filter = ['ingredient_group__title']
    # search_fields = ['title', 'ingredient_group__title', ]
    pass


class MenuItemAdmin(admin.ModelAdmin):
    # ordering = ['title', 'recipe']
    # list_display = ['recipe', 'title']
    # list_filter = ['recipe__title']
    # search_fields = ['title', 'recipe__title', ]
    pass


admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
