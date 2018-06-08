#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from v1.recipe.models import Recipe


class Rating(models.Model):
    """
    Django Model to hold a Rating of a recipe.
    Ratings share a many to one relationship.
    Meaning each Recipe will have many Ratings.
    :author: = User that created the comment
    :recipe: = The recipe the comment is related to
    :comment: = A comment on the recipe
    :rating: = A rating 1-5
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    comment = models.CharField(_('comment'), max_length=250)
    # TODO: add a range requirement
    # if 'rating' in validated_data:
    #     rating = int(validated_data.get('rating', 0))
    #     if rating < 0:
    #         rating = 0
    #     elif rating > 5:
    #         rating = 5
    #     validated_data['rating'] = rating

    rating = models.IntegerField(_('rating'), default=0)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return '%s - %s' % (self.rating, self.comment)
