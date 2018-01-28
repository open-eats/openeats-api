#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from v1.recipe.models import Recipe


class IngredientGroup(models.Model):
    """
    Django Model to hold an Ingredient Groups.
    Ingredient Groups share a many to one relationship.
    Meaning each Recipe will have many Ingredient Groups.
    :title: = Title of the Ingredient Group (EX: Cheddar Biscuits)
    """
    title = models.CharField(_('title'), max_length=150, null=True, blank=True)
    recipe = models.ForeignKey(Recipe, verbose_name=_('recipe'), related_name='ingredient_groups')

    class Meta:
        ordering = ['id']
        unique_together = ('title', 'recipe')

    def __unicode__(self):
        return '%s' % self.title


class Ingredient(models.Model):
    """
    Django Model to hold an Ingredient.
    Ingredients share a many to one relationship.
    Meaning each Ingredient Group will have many Ingredients.
    :title: = Title of the Ingredient (EX: Flour)
    :quantity: = Title of the Ingredient (EX: 200, 15, 2)
    :measurement: = Title of the Ingredient (EX: Liters, Cups, Grams, tablespoons)
    """
    title = models.CharField(_('title'), max_length=250)
    quantity = models.FloatField(_('quantity'), default=0)
    measurement = models.CharField(_('measurement'), max_length=200, blank=True, null=True)
    ingredient_group = models.ForeignKey(IngredientGroup, verbose_name=_('IngredientGroup'), related_name='ingredients', null=True)
 
    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return '%s' % self.title
