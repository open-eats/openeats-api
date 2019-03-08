#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers
import pytz
from datetime import datetime

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
            'start_date',
            'complete_date',
            'recipe',
            'recipe_data',
        ]
        extra_kwargs = {'recipe': {'write_only': True}}

    def create(self, validated_data):
        if validated_data.get('complete'):
            validated_data['complete_date'] = datetime.now(pytz.utc)
        return super(MenuItemSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('complete') and not instance.complete:
            validated_data['complete_date'] = datetime.now(pytz.utc)
        return super(MenuItemSerializer, self).update(instance, validated_data)
