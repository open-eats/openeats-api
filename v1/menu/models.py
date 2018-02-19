#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from v1.recipe.models import Recipe


class Menu(models.Model):
    """
    Django Model to hold an Menus.
    """
    title = models.CharField(_('title'), max_length=150, null=True, blank=True)
    description = models.CharField(_('description'), max_length=150, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return '%s' % self.title


class MenuItem(models.Model):
    """
    Django Model to hold a Recipe that is related to a menu.
    """
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='menu_recipe')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return '%s' % self.recipe.title
