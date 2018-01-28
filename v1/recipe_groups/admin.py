#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.contrib import admin
from .models import Cuisine, Course, Tag


class CourseAndCuisineAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ['title']
    list_filter = ['author']


class TagAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ['title']
    list_filter = ['recipe__title']


admin.site.register(Course, CourseAndCuisineAdmin)
admin.site.register(Cuisine, CourseAndCuisineAdmin)
admin.site.register(Tag, TagAdmin)
