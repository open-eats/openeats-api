#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.serializers import ImageField
from rest_framework.settings import api_settings
from rest_framework.fields import SerializerMethodField


from v1.recipe.models import Recipe, SubRecipe
from v1.recipe_groups.models import Tag
from v1.ingredient.serializers import IngredientGroupSerializer
from v1.recipe_groups.serializers import TagSerializer
from v1.ingredient.models import IngredientGroup, Ingredient
from v1.recipe.mixins import FieldLimiter


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


class SubRecipeSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    title = serializers.ReadOnlyField(source='child_recipe.title')

    class Meta:
        model = SubRecipe
        fields = (
            'quantity',
            'measurement',
            'title',
            'child_recipe_id',
        )


class MiniBrowseSerializer(FieldLimiter, serializers.ModelSerializer):
    """ Used to get random recipes and limit the return data. """
    photo_thumbnail = CustomImageField(required=False)
    pub_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
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
    subrecipes = SerializerMethodField()
    pub_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    update_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    username = serializers.ReadOnlyField(source='author.username')

    def get_subrecipes(self, obj):
        try:
            subrecipes = SubRecipe.objects.filter(parent_recipe_id=obj.id)
            return [SubRecipeSerializer(subrecipe).data for subrecipe in subrecipes]
        except:
            return {}

    class Meta:
        model = Recipe
        exclude = ('slug',)

    def update(self, instance, validated_data):
        """
        Update and return a new `Recipe` instance, given the validated data.
        This will also update or create all the ingredient,
        or tag objects required.
        """
        # Pop tags, and ingredients
        ingredient_data = validated_data.pop('ingredient_groups', None)
        tag_data = validated_data.pop('tags', None)
        # ManytoMany fields in django rest don't work very well, so we are getting the data directly fron teh context
        subrecipe_data = None
        if 'request' in self.context:
            subrecipe_data = self.context['request'].data.get('subrecipes')

        if 'rating' in validated_data:
            rating = int(validated_data.get('rating', 0))
            if rating < 0:
                rating = 0
            elif rating > 5:
                rating = 5
            validated_data['rating'] = rating

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Create the Ingredients
        # TODO: don't delete everything when we edit the recipe. Use an ID.
        if ingredient_data:
            for ingredient_group in instance.ingredient_groups.all():
                for ingredient in ingredient_group.ingredients.all():
                    ingredient.delete()
                ingredient_group.delete()

            for ingredient_group in ingredient_data:
                group = IngredientGroup.objects.create(
                    recipe=instance, title=ingredient_group.get('title')
                )
                for ingredient in ingredient_group.get('ingredients'):
                    Ingredient.objects.create(
                        ingredient_group=group, **ingredient
                    )

        # Create the Tags
        # TODO: don't delete everything when we edit the recipe. Use an ID.
        if tag_data:
            for tag in instance.tags.all():
                instance.tags.remove(tag)

            for tag in tag_data:
                obj, created = Tag.objects.get_or_create(title=tag['title'].strip())
                instance.tags.add(obj)

        # Create the sub-recipes
        # TODO: don't delete everything when we edit the recipe. Use an ID.
        if subrecipe_data:
            for subrecipe in SubRecipe.objects.filter(parent_recipe=instance):
                subrecipe.delete()

            for subrecipe in subrecipe_data:
                if subrecipe.get('title'):
                    recipe = Recipe.objects.filter(title=subrecipe.get('title', '')).first()
                    if recipe:
                        obj = SubRecipe.objects.create(
                            quantity=subrecipe.get('quantity', ''),
                            measurement=subrecipe.get('measurement', ''),
                            child_recipe=recipe,
                            parent_recipe=instance
                        )
                        obj.save()

        instance.save()
        return instance

    def create(self, validated_data):
        """
        Create and return a new `Recipe` instance, given the validated data.
        This will also create all the ingredient objects required and
        Create all Tags that are new.
        """
        # Pop tags, and ingredients
        ingredient_data = validated_data.pop('ingredient_groups', None)
        tag_data = validated_data.pop('tags', None)
        # ManytoMany fields in django rest don't work very well, so we are getting the data directly fron teh context
        subrecipe_data = None
        if 'request' in self.context:
            subrecipe_data = self.context['request'].data.get('subrecipes')

        if 'rating' in validated_data:
            rating = int(validated_data.get('rating', 0))
            if rating < 0:
                rating = 0
            elif rating > 5:
                rating = 5
            validated_data['rating'] = rating

        # Create the recipe.
        # Use the log-in user as the author.
        recipe = Recipe.objects.create(
            author=self.context['request'].user,
            **validated_data
        )

        # Create the Ingredients
        for ingredient_group in ingredient_data:
            group = IngredientGroup.objects.create(
                recipe=recipe, title=ingredient_group.get('title')
            )
            for ingredient in ingredient_group.get('ingredients'):
                Ingredient.objects.create(ingredient_group=group, **ingredient)

        # Create the Tags
        if tag_data:
            for tag in tag_data:
                obj, created = Tag.objects.get_or_create(title=tag['title'].strip())
                recipe.tags.add(obj)

        # Create the sub-recipes
        if subrecipe_data:
            for subrecipe in subrecipe_data:
                if subrecipe.get('title'):
                    child_recipe = Recipe.objects.filter(title=subrecipe.get('title', '')).first()
                    if child_recipe:
                        obj = SubRecipe.objects.create(
                            quantity=subrecipe.get('quantity', ''),
                            measurement=subrecipe.get('measurement', ''),
                            child_recipe=child_recipe,
                            parent_recipe=recipe
                        )
                        obj.save()

        return recipe


class RatingSerializer(serializers.ModelSerializer):
    """ Standard `rest_framework` ModelSerializer """
    total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('rating', 'total')