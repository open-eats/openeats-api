#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from v1.recipe.models import Recipe


class GroceryList(models.Model):
    """
    The GroceryList is the core of list app.
    It offers a home to many GroceryItems.
    title = The name of the GroceryList.
    slug = The HTML safe name of the GroceryList.
    author = The User who created the GroceryList.
    pub_date = The date that the GroceryList was created on.
    """
    title = models.CharField(_("grocery list title"), max_length=250)
    slug = AutoSlugField(_('slug'), populate_from='title')
    author = models.ForeignKey(User, verbose_name=_('user'))
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __unicode__(self):
        return '%s' % self.title

    def item_count(self):
        """get the number of items in the list"""
        return GroceryItem.objects.filter(list=self).count()


class GroceryItem(models.Model):
    """
    The GroceryItem is an item on a GroceryList.
    list = The GroceryList that owns the GroceryItem.
    title = The name of the GroceryItem.
    completed = Whether or not the GroceryItem has been purchased or
                added to the users shopping cart in the supermarket.
    """
    list = models.ForeignKey(GroceryList, verbose_name=_('grocery_list'), related_name='items')
    title = models.CharField(_("title"), max_length=550)
    completed = models.BooleanField(_("completed"), default=False)

    class Meta:
        ordering = ['pk']

    def __unicode__(self):
        return '%s' % self.title


class GroceryShared(models.Model):
    """
    Determines whether or not a GroceryList is shared to another user.
    Shared lists allow other uses to add/delete/edit the GroceryList.
    list = The GroceryList to be shared.
    shared_by = The User that shared the List.
    shared_to = The User that is given access to a GroceryList.
    """
    list = models.ForeignKey(GroceryList, verbose_name=_('grocery list'))
    shared_by = models.ForeignKey(User, verbose_name=_('shared by'), related_name="shared_by")
    shared_to = models.ForeignKey(User, verbose_name=_('shared to'), related_name="shared_to")

    def __unicode__(self):
        return '%s' % self.list.title


class GroceryRecipe(models.Model):
    """
    This model links a GroceryList to a Recipe.
    list = The GroceryList has holds the Recipe.
    recipe = The Recipe that is on a GroceryList.
    """
    list = models.ForeignKey(GroceryList, verbose_name=_('grocery list'))
    recipe = models.ForeignKey(Recipe, verbose_name=_('recipe'))

    def __unicode__(self):
        return '%s' % self.recipe.title
