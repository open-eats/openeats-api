#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers

from v1.recipe.mixins import FieldLimiter
from v1.recipe.serializers import MiniBrowseSerializer
from .models import MenuItem


class MenuItemSerializer(FieldLimiter, serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    recipe_data = MiniBrowseSerializer(read_only=True, source='recipe')
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

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
            'recipe_data',
        ]
        extra_kwargs = {'recipe': {'write_only': True}}
