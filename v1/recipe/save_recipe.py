#!/usr/bin/env python
# encoding: utf-8

from django.db.models import Count
from django.core.exceptions import FieldDoesNotExist
from v1.recipe.models import Recipe, SubRecipe
from v1.recipe_groups.models import Tag, Course, Cuisine
from v1.ingredient.models import IngredientGroup, Ingredient


class SaveRecipe(object):
    def __init__(self, data, author, instance=None):
        # Extract the data from data for use in the saving process
        self.author = author
        self.ingredients = data.pop('ingredient_groups', None)
        self.tags = data.pop('tags', None)
        self.course = data.pop('course', None)
        self.cuisine = data.pop('cuisine', None)
        self.subrecipes = data.pop('subrecipes', None)
        self.data = data

        # Save the data
        self._save_course()
        self._save_cuisine()
        self.recipe = self.update(instance) if instance else self.create()
        self._save_ingredient_data()
        self._save_subrecipe_data()
        self._save_tags()
        self._delete_recipe_groups()

    def _save_course(self):
        if self.course:
            if self.course.get('id'):
                self.data['course'] = Course.objects.get(id=self.course.get('id'))
            elif self.course.get('title'):
                self.data['course'], created = Course.objects.get_or_create(
                    title=self.course.get('title'),
                    defaults={'author': self.author},
                )

    def _save_cuisine(self):
        if self.cuisine:
            if self.cuisine.get('id'):
                self.data['cuisine'] = Cuisine.objects.get(id=self.cuisine.get('id'))
            elif self.cuisine.get('title'):
                self.data['cuisine'], created = Cuisine.objects.get_or_create(
                    title=self.cuisine.get('title'),
                    defaults={'author': self.author},
                )

    def _delete_recipe_groups(self):
            # Check to see if we have any Cuisines or Courses with no recipes associated with them.
            # Id we do, delete them.
            Cuisine.objects.all().annotate(total=Count('recipe', distinct=True)).filter(total=0).delete()
            Course.objects.all().annotate(total=Count('recipe', distinct=True)).filter(total=0).delete()

    def _save_tags(self):
        if self.tags:
            # TODO: don't delete everything when we edit the recipe. Use an ID.
            for tag in self.recipe.tags.all():
                self.recipe.tags.remove(tag)

            for tag in self.tags:
                obj, created = Tag.objects.get_or_create(title=tag['title'].strip())
                self.recipe.tags.add(obj)

    def _save_ingredient_data(self):
        if self.ingredients:
            # TODO: don't delete everything when we edit the recipe. Use an ID.
            for ingredient_group in self.recipe.ingredient_groups.all():
                for ingredient in ingredient_group.ingredients.all():
                    ingredient.delete()
                ingredient_group.delete()

            for ingredient_group in self.ingredients:
                group = IngredientGroup.objects.create(
                    recipe=self.recipe, title=ingredient_group.get('title')
                )
                for ingredient in ingredient_group.get('ingredients'):
                    ingredient.pop('id') if ingredient.get('id') else None
                    Ingredient.objects.create(
                        ingredient_group=group, **ingredient
                    )

    def _save_subrecipe_data(self):
        if self.subrecipes:
            for subrecipe in SubRecipe.objects.filter(parent_recipe=self.recipe):
                subrecipe.delete()

            for subrecipe in self.subrecipes:
                if subrecipe.get('title'):
                    recipe = Recipe.objects.filter(title=subrecipe.get('title', '')).first()
                    if recipe:
                        obj = SubRecipe.objects.create(
                            quantity=subrecipe.get('quantity', ''),
                            measurement=subrecipe.get('measurement', ''),
                            child_recipe=recipe,
                            parent_recipe=self.recipe
                        )
                        obj.save()

    def clean_data(self):
        """
        Clean up the data before we try and save it into the Recipe model
        :return:
        """
        for key in ['author', 'id', 'slug']:
            self.data.pop(key) if self.data.get(key) is not None else None

        keys = []
        for key, value in self.data.items():
            try:
                Recipe._meta.get_field(key)
            except FieldDoesNotExist:
                keys.append(key)

        for key in keys:
            self.data.pop(key)

    def update(self, instance):
        """
        Update and return a new `Recipe` instance, given the validated data.
        This will also update or create all the ingredient,
        or tag objects required.
        """
        self.clean_data()
        for attr, value in self.data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def create(self):
        """
        Create and return a new `Recipe` instance, given the validated data.
        This will also create all the ingredient objects required and
        Create all Tags that are new.
        """
        self.clean_data()
        recipe = Recipe.objects.create(
            author=self.author,
            **self.data
        )

        # {'public': True, 'title': 'qwe', 'info': 'qwe', 'directions': 'qwe', 'prep_time': '1', 'cook_time': '1',
        #  'servings': '1', 'rating': '1'}

        return recipe

    def get_recipe(self):
        """
        Create and return a new `Recipe` instance, given the validated data.
        This will also create all the ingredient objects required and
        Create all Tags that are new.
        """
        return self.recipe
