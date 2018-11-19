#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers
from rest_framework.serializers import ImageField
from rest_framework.settings import api_settings
from rest_framework.fields import SerializerMethodField

from v1.recipe.models import Recipe, SubRecipe
from v1.ingredient.serializers import IngredientGroupSerializer
from v1.recipe_groups.serializers import TagSerializer, CourseSerializer, CuisineSerializer
from v1.recipe.mixins import FieldLimiter
from v1.rating.average_rating import average_rating


class CustomImageField(ImageField):
    def to_representation(self, value):
        use_url = getattr(self, 'use_url', api_settings.UPLOADED_FILES_USE_URL)
        try:
            if not value:
                return None
        except:
            return None

        if use_url:
            if not getattr(value, 'url', None):
                # If the file has not been saved it may not have a URL.
                return None
            url = value.url
            request = self.context.get('request', None)
            if request is not None:
                return request.build_absolute_uri(url)
            return url

        return super(ImageField, self).to_representation(value)


class RecipeSlug(serializers.Serializer):
    def to_representation(self, value):
        try:
            return value.slug
        except:
            return super(RecipeSlug, self).to_representation(value)

    def to_internal_value(self, data):
        try:
            return Recipe.objects.get(slug=data)
        except:
            return super(RecipeSlug, self).to_internal_value(data)


class AverageRating(serializers.ReadOnlyField):
    def to_representation(self, value):
        return average_rating(value)


class SubRecipeSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    slug = serializers.ReadOnlyField(source='child_recipe.slug')
    title = serializers.ReadOnlyField(source='child_recipe.title')

    class Meta:
        model = SubRecipe
        fields = (
            'child_recipe_id',
            'slug',
            'quantity',
            'measurement',
            'title',
        )


class MiniBrowseSerializer(FieldLimiter, serializers.ModelSerializer):
    """ Used to get random recipes and limit the return data. """
    photo_thumbnail = CustomImageField(required=False)
    pub_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    rating = AverageRating(source='id')

    class Meta:
        model = Recipe
        fields = (
            'id',
            'slug',
            'title',
            'pub_date',
            'rating',
            'photo_thumbnail',
            'info'
        )


class RecipeSerializer(FieldLimiter, serializers.ModelSerializer):
    """ Used to create new recipes"""
    photo = CustomImageField(required=False)
    photo_thumbnail = CustomImageField(required=False)
    ingredient_groups = IngredientGroupSerializer(many=True)
    tags = TagSerializer(many=True, required=False)
    rating = AverageRating(source='id')
    subrecipes = SerializerMethodField()
    pub_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    update_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    username = serializers.ReadOnlyField(source='author.username')
    course = CourseSerializer()
    cuisine = CuisineSerializer()

    def get_subrecipes(self, obj):
        try:
            subrecipes = SubRecipe.objects.filter(parent_recipe_id=obj.id)
            return [SubRecipeSerializer(subrecipe).data for subrecipe in subrecipes]
        except:
            return {}

    class Meta:
        model = Recipe
        fields = '__all__'
