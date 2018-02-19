#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers
from rest_framework.fields import CharField

from v1.recipe.mixins import FieldLimiter
from .models import Menu, MenuItem


class MenuItemSerializer(FieldLimiter, serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    recipe_title = CharField(source='recipe.title', read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id',
            'recipe_title',
            'menu',
            'recipe',
            'all_day',
            'start_date',
            'end_date',
        ]


class MenuSerializer(FieldLimiter, serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    menu = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = [
            'id',
            'title',
            'description',
            'author',
            'menu',
        ]

