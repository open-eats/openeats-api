#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers
from rest_framework.fields import CharField

from v1.recipe.mixins import FieldLimiter
from v1.recipe.serializers import MiniBrowseSerializer
from .models import MenuItem


class MenuItemSerializer(FieldLimiter, serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    # recipe = MiniBrowseSerializer(required=False)
    recipe_title = CharField(source='recipe.title', read_only=True)
    recipe_slug = CharField(source='recipe.slug', read_only=True)
    recipe_pub_date = CharField(source='recipe.pub_date', read_only=True)
    recipe_rating = CharField(source='recipe.rating', read_only=True)
    recipe_photo_thumbnail = CharField(source='recipe.photo_thumbnail', read_only=True)
    recipe_info = CharField(source='recipe.info', read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id',
            'author',
            'complete',
            'recipe',
            'all_day',
            'start_date',
            'end_date',

            'recipe',
            'recipe_title',
            'recipe_slug',
            'recipe_pub_date',
            'recipe_rating',
            'recipe_photo_thumbnail',
            'recipe_info'
        ]
