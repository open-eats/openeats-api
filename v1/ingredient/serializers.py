#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Ingredient, IngredientGroup


class IngredientSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    class Meta:
        model = Ingredient
        fields = ['id', 'quantity', 'measurement', 'title']


class IngredientGroupSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = IngredientGroup
        fields = ['id', 'title', 'ingredients']
