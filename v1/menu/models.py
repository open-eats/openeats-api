#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from v1.recipe.models import Recipe


class Menu(models.Model):
    """
    Django Model to hold an Menus.
    Ingredient Groups share a many to one relationship.
    Meaning each Recipe will have many Ingredient Groups.
    :title: = Title of the Ingredient Group (EX: Cheddar Biscuits)
    """
    title = models.CharField(_('title'), max_length=150, null=True, blank=True)
    description = models.CharField(_('description'), max_length=150, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return '%s' % self.title


class MenuItem(models.Model):
    """
    Django Model to hold an Recipe that is related to a menu.
    :occurrence: = When the user is planning to make the recipe. (EX: Monday, Breakfest, Lunch, Dinner)
    """
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='menu_recipe')
    occurrence = models.CharField(_('type'), max_length=150, null=True, blank=True)
    date = models.DateTimeField()

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return '%s' % self.recipe.title
