#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from graphene import Int, Connection


def total_count(_type):
    class Con(Connection):
        total_count = Int()

        class Meta:
            name = _type._meta.name + 'Connection'
            node = _type

        def resolve_total_count(self, args, context, info):
            return self.length

    return Con
