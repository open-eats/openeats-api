#!/usr/bin/env python
# encoding: utf-8

from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        from . import signals
