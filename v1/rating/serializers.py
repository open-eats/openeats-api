#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers

from v1.recipe.serializers import RecipeSlug
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    recipe = RecipeSlug()
    user_id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Rating
        fields = [
            'id',
            'rating',
            'comment',
            'recipe',
            'user_id',
            'username',
            'author'
        ]

    def update(self, instance, validated_data):
        if 'rating' in validated_data:
            rating = int(validated_data.get('rating', 0))
            if rating < 0:
                rating = 0
            elif rating > 5:
                rating = 5
            validated_data['rating'] = rating
        return super(RatingSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        if 'rating' in validated_data:
            rating = int(validated_data.get('rating', 0))
            if rating < 0:
                rating = 0
            elif rating > 5:
                rating = 5
            validated_data['rating'] = rating
        return super(RatingSerializer, self).create(validated_data)
