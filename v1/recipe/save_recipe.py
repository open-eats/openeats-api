#!/usr/bin/env python
# encoding: utf-8

from django.db.models import Count
from django.core.exceptions import FieldDoesNotExist
from rest_framework.exceptions import ParseError

from v1.recipe.models import Recipe, SubRecipe
from v1.recipe_groups.models import Tag, Course, Cuisine
from v1.ingredient.models import IngredientGroup, Ingredient


class Validators(object):
    def __init__(self, partial=False):
        self.partial = partial

    def required(self, item):
        if not self.partial:
            return None if item else "This item is required."
        return None

    def is_digit(self, item):
        if self.partial and item is None:
            return None
        try:
            int(item)
        except:
            return "This item must be a number."
        return None


class SaveRecipe(Validators):
    def __init__(self, data, author, partial=False):
        super(SaveRecipe, self).__init__(partial=partial)

        # Extract the data from data for use in the saving process
        self.author = author
        self.data = data

        # Remove bad fields from the data
        self._clean_data()

        # Check the data from any errors
        self._validate()

        # Remove the complex data objects from processing
        self.tags = self.data.pop('tags', None)
        self.course = self.data.pop('course', None)
        self.cuisine = self.data.pop('cuisine', None)
        self.subrecipes = self.data.pop('subrecipes', None)
        self.ingredients = self.data.pop('ingredient_groups', None)

    def _save_course(self):
        """
        Add the Course instance to the self.data dict for use when we save the recipe
        If the Course doesn't exist create a new one.
        """
        if self.course:
            # Lookup the course by ID. If the ID isn't there, lookup by title
            # if that isn't found, create it.
            if self.course.get('id'):
                self.data['course'] = Course.objects.get(id=self.course.get('id'))
            elif self.course.get('title'):
                self.data['course'], created = Course.objects.get_or_create(
                    title=self.course.get('title'),
                    defaults={'author': self.author},
                )

    def _save_cuisine(self):
        """
        Add the Cuisine instance to the self.data dict for use when we save the recipe.
        If the Cuisine doesn't exist create a new one.
        """
        if self.cuisine:
            # Lookup the cuisine by ID. If the ID isn't there, lookup by title
            # if that isn't found, create it.
            if self.cuisine.get('id'):
                self.data['cuisine'] = Cuisine.objects.get(id=self.cuisine.get('id'))
            elif self.cuisine.get('title'):
                self.data['cuisine'], created = Cuisine.objects.get_or_create(
                    title=self.cuisine.get('title'),
                    defaults={'author': self.author},
                )

    @staticmethod
    def _delete_recipe_groups():
            # Check to see if we have any Cuisines or Courses with no recipes associated with them.
            # Id we do, delete them.
            Cuisine.objects.all().annotate(total=Count('recipe', distinct=True)).filter(total=0).delete()
            Course.objects.all().annotate(total=Count('recipe', distinct=True)).filter(total=0).delete()

    def _save_tags(self, recipe):
        if self.tags:
            # TODO: don't delete everything when we edit the recipe. Use an ID.
            for tag in recipe.tags.all():
                recipe.tags.remove(tag)

            for tag in self.tags:
                obj, created = Tag.objects.get_or_create(title=tag['title'].strip())
                recipe.tags.add(obj)

    def _save_ingredient_data(self, recipe):
        if self.ingredients:
            # TODO: don't delete everything when we edit the recipe. Use an ID.
            for ingredient_group in recipe.ingredient_groups.all():
                for ingredient in ingredient_group.ingredients.all():
                    ingredient.delete()
                ingredient_group.delete()

            for ingredient_group in self.ingredients:
                group = IngredientGroup.objects.create(
                    recipe=recipe, title=ingredient_group.get('title')
                )
                for ingredient in ingredient_group.get('ingredients'):
                    ingredient.pop('id') if ingredient.get('id') else None
                    Ingredient.objects.create(
                        ingredient_group=group, **ingredient
                    )

    def _save_subrecipe_data(self, recipe):
        if self.subrecipes:
            for subrecipe in SubRecipe.objects.filter(parent_recipe=recipe):
                subrecipe.delete()

            for subrecipe in self.subrecipes:
                if subrecipe.get('title'):
                    child_recipe = Recipe.objects.filter(title=subrecipe.get('title', '')).first()
                    if recipe:
                        obj = SubRecipe.objects.create(
                            numerator=subrecipe.get('numerator', 0),
                            denominator=subrecipe.get('denominator', 1),
                            measurement=subrecipe.get('measurement', ''),
                            child_recipe=child_recipe,
                            parent_recipe=recipe
                        )
                        obj.save()

    def _clean_data(self):
        """
        Clean up the data before we try and save it into the Recipe model.
        Remove fields that not not apart of the model or shouldn't be saved.
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

    def _validate(self):
        fields = {
            "title": [self.required],
            "directions": [self.required],

            "servings": [self.required, self.is_digit],
            "prep_time": [self.required, self.is_digit],
            "cook_time": [self.required, self.is_digit],

            "ingredient_groups": [self.required],
            "cuisine": [self.required],
            "course": [self.required],
        }

        errors = {}
        for key, validators in fields.items():
            for validator in validators:
                error = validator(self.data.get(key))
                if error:
                    errors[key] = [error]
                    # Only send one error at a time
                    break

        if len(errors) > 0:
            raise ParseError(errors)

    def update(self, instance):
        """ Update and return a new `Recipe` instance, given the validated data """
        self._save_course()
        self._save_cuisine()
        for attr, value in self.data.items():
            setattr(instance, attr, value)
        self._save_ingredient_data(instance)
        self._save_subrecipe_data(instance)
        self._save_tags(instance)
        instance.save()

        self._delete_recipe_groups()

        return instance

    def create(self):
        """ Create and return a new `Recipe` instance, given the validated data """
        self._save_course()
        self._save_cuisine()
        recipe = Recipe.objects.create(
            author=self.author,
            **self.data
        )
        self._save_ingredient_data(recipe)
        self._save_subrecipe_data(recipe)
        self._save_tags(recipe)
        self._delete_recipe_groups()

        return recipe
