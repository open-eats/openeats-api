#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers
from rest_framework.fields import CharField

from .models import Menu, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    recipe_title = CharField(source='recipe.title', read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id',
            'recipe_title',
            'menu',
            'recipe',
            'occurrence',
            'date',
        ]


class MenuSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    menu = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = [
            'id',
            'title',
            'description',
            'user',
            'start_date',
            'end_date',
            'pub_date',
            'menu',
            'update_date'
        ]

