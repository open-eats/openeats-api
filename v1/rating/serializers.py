#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """

    class Meta:
        model = Rating
        fields = [
            'id',
            'rating',
            'comment',
            'recipe',
            'author'
        ]
