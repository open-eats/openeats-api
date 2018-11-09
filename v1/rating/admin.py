#!/usr/bin/env python
# encoding: utf-8

from django.contrib import admin
from .models import Rating


class RatingAdmin(admin.ModelAdmin):
    ordering = ['id', 'rating']
    list_display = ['rating', 'comment', 'recipe', 'author']
    list_filter = ['recipe', 'author']
    search_fields = ['rating', 'comment', ]


admin.site.register(Rating, RatingAdmin)
