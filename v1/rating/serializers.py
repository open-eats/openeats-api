#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers

from v1.recipe.serializers import RecipeSlug
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    recipe = RecipeSlug()
    username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Rating
        fields = [
            'id',
            'rating',
            'comment',
            'recipe',
            'username',
            'author'
        ]
