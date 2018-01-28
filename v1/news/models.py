#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext_lazy as _


class News(models.Model):
    """
    Django Model to hold News that will display on the homepage.
    :title: = Title of the News
    :content: = A short description of the news
    :frontpage: = True if it should be displayed on the homepage
    :image: = Large background image for the homepage
    :pub_date: = Date created
    """
    title = models.CharField(_('title'), max_length=191, unique=True)
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)
    content = models.TextField(_('content'), blank=True)
    frontpage = models.BooleanField(_('frontpage'), default=False,
                                    help_text="determines if the story appears on the front page")
    image = models.ImageField(_('image'), upload_to='uploads/news/', blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)

    def __unicode__(self):
        return '%s' % self.title
