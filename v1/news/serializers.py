#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    class Meta:
        model = News
        exclude = ('slug', 'pub_date',)
