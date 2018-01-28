#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.contrib import admin
from .models import Recipe, SubRecipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'pub_date']
    list_filter = ['author', 'course', 'cuisine']
    search_fields = ['author__username', 'title',]


class SubRecipeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(SubRecipe, SubRecipeAdmin)
