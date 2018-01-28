#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from v1.recipe_groups.models import Cuisine, Course, Tag


class Recipe(models.Model):
    """
    Django Model to hold Recipes.

    Courses have a one to Many relation with Recipes.
    Cuisines have a one to Many relation with Recipes.
    Tags have a Many to Many relation with Recipes.
    Ingredient Groups have a Many to one relation with Recipes.
    Subrecipes have a Many to Many relation with Recipes. 
        They allow another recipe to be show in the Ingredient section.

    :title: = Title of the Recipe
    :author: = Creator of the Recipe
    :photo: = Raw Image of a Recipe
    :photo_thumbnail: = compressed image of the photo
    :info: = Description of the recipe
    :directions: = How to make the recipe
    :prep_time: = How long it takes to prepare the recipe
    :cook_time: = How long the recipe takes to cook
    :servings: = How many people the recipe with serve
    :rating: = Rating of the recipe
    :pub_date: = When the recipe was created
    :update_date: = When the recipe was updated
    """
    title = models.CharField(_("Recipe Title"), max_length=250)
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)
    author = models.ForeignKey(User, verbose_name=_('user'), null=True)
    photo = models.ImageField(_('photo'), blank=True, upload_to="upload/recipe_photos")
    photo_thumbnail = ImageSpecField(source='photo',
                                     processors=[ResizeToFill(300, 200)],
                                     format='JPEG',
                                     options={'quality': 70})
    cuisine = models.ForeignKey(Cuisine, verbose_name=_('cuisine'))
    course = models.ForeignKey(Course, verbose_name=_('course'))
    tags = models.ManyToManyField(Tag, verbose_name=_('tag'), blank=True)
    subrecipes = models.ManyToManyField('self', verbose_name=_('subrecipes'), through='SubRecipe', symmetrical=False)
    info = models.TextField(_('info'), help_text="enter information about the recipe", blank=True)
    directions = models.TextField(_('direction_text'), help_text="directions", blank=True)
    source = models.CharField(_('course'), max_length=200, blank=True)
    prep_time = models.IntegerField(_('prep time'), help_text="enter time in minutes")
    cook_time = models.IntegerField(_('cook time'), help_text="enter time in minutes")
    servings = models.IntegerField(_('servings'), help_text="enter total number of servings")
    rating = models.IntegerField(_('rating'), help_text="rating of the meal", default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=True)

    class Meta:
        ordering = ['-pub_date', 'title']

    def __unicode__(self):
        return '%s' % self.title


class SubRecipe(models.Model):
    quantity = models.IntegerField(_('quantity'), blank=True, null=True)
    measurement = models.TextField(_('measurement'), blank=True, null=True)
    child_recipe = models.ForeignKey("Recipe", verbose_name=_('subrecipe'), related_name='child_recipe', null=True)
    parent_recipe = models.ForeignKey("Recipe", verbose_name=_('parent_recipe'), related_name='parent_recipe', null=True)

    def __unicode__(self):
        return '%s' % self.parent_recipe.title
