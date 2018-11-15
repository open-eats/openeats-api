#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers
from rest_framework.serializers import ImageField
from rest_framework.settings import api_settings
from rest_framework.fields import SerializerMethodField

from v1.recipe.models import Recipe, SubRecipe
from v1.recipe_groups.models import Tag, Course, Cuisine
from v1.ingredient.serializers import IngredientGroupSerializer
from v1.recipe_groups.serializers import TagSerializer, CourseSerializer, CuisineSerializer
from v1.ingredient.models import IngredientGroup, Ingredient
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

    def update(self, instance, validated_data):
        """
        Update and return a new `Recipe` instance, given the validated data.
        This will also update or create all the ingredient,
        or tag objects required.
        """
        # Pop tags, and ingredients
        ingredient_data = validated_data.pop('ingredient_groups', None)
        tag_data = validated_data.pop('tags', None)
        course = validated_data.pop('course', None)
        cuisine = validated_data.pop('cuisine', None)
        print(course)
        print(cuisine)

        # If the course is a string.
        # Create a new course and replace it with a string
        if course.get('id'):
            validated_data['course'] = Course.objects.get(id=course.get('id'))
        elif course.get('title'):
            validated_data['course'] = Course.objects.create(
                author=self.context['request'].user,
                title=course.get('title')
            ).save()
        #TODO: on update check if there are any of the old course left.
        # if not delete them

        # If the cuisine is a string.
        # Create a new cuisine and replace it with a string
        if cuisine.get('id'):
            validated_data['cuisine'] = Cuisine.objects.get(id=course.get('id'))
        elif cuisine.get('title'):
            validated_data['cuisine'] = Cuisine.objects.create(
                author=self.context['request'].user,
                title=course.get('title')
            ).save()

        # ManytoMany fields in django rest don't work very well, so we are getting the data directly fron teh context
        subrecipe_data = None
        if 'request' in self.context:
            subrecipe_data = self.context['request'].data.get('subrecipes')

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
        course = validated_data.pop('course', None)
        cuisine = validated_data.pop('cuisine', None)
        validated_data.pop('author')

        # If the course is a string.
        # Create a new course and replace it with a string
        if course.get('id'):
            validated_data['course'] = Course.objects.get(id=course.get('id'))
        elif course.get('title'):
            validated_data['course'] = Course.objects.create(
                author=self.context['request'].user,
                title=course.get('title')
            ).save()
        #TODO: on update check if there are any of the old course left.
        # if not delete them

        # If the cuisine is a string.
        # Create a new cuisine and replace it with a string
        if cuisine.get('id'):
            validated_data['cuisine'] = Cuisine.objects.get(id=course.get('id'))
        elif cuisine.get('title'):
            validated_data['cuisine'] = Cuisine.objects.create(
                author=self.context['request'].user,
                title=course.get('title')
            ).save()

        # ManytoMany fields in django rest don't work very well, so we are getting the data directly fron teh context
        subrecipe_data = None
        if 'request' in self.context:
            subrecipe_data = self.context['request'].data.get('subrecipes')

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
