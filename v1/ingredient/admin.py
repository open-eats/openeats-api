#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.contrib import admin
from v1.ingredient.models import Ingredient, IngredientGroup


class IngredientAdmin(admin.ModelAdmin):
    ordering = ['title', 'ingredient_group']
    list_display = ['title', 'quantity', 'measurement']
    list_filter = ['ingredient_group__title']
    search_fields = ['title', 'ingredient_group__title', ]


class IngredientGroupAdmin(admin.ModelAdmin):
    ordering = ['title', 'recipe']
    list_display = ['recipe', 'title']
    list_filter = ['recipe__title']
    search_fields = ['title', 'recipe__title', ]

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientGroup, IngredientGroupAdmin)
