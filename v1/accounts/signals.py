#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def init_new_user(sender, instance, signal, created, **kwargs):
    """ Create tokens for user that login in successfully """
    if created:
        Token.objects.create(user=instance)
