#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers
from .models import Cuisine, Course, Tag


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
        )


class CuisineSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Cuisine
        fields = (
            'id',
            'author',
            'title',
        )


class AggCuisineSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cuisine
        fields = '__all__'


class AggCourseSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    class Meta:
        model = Tag
        fields = (
            'id',
            'title',
        )
