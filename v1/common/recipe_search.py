#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import operator
from functools import reduce
from django.db import models


def get_search_results(search_fields, queryset, search_term):
    """
    This code mirrors the search functionality that the django admin pages uses.
    It also happens to match what django rest users for there search implementation.
    https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
    
    Usage: Returns a queryset to implement the search.
    Example:
        query = get_search_results(
            django_model_search_field_list (search_fields)
            django_queryset (queryset),
            search_keyword_string (search_term)
        )
        query = get_search_results(
            ['title', 'ingredients__title', 'tags__title'],
            django_queryset,
            'chicken taco'
        )
    """

    # Apply keyword searches.
    def construct_search(field_name):
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    if search_fields and search_term:
        orm_lookups = [construct_search(str(search_field))
                       for search_field in search_fields]
        for bit in search_term.split():
            or_queries = [models.Q(**{orm_lookup: bit})
                          for orm_lookup in orm_lookups]
            queryset = queryset.filter(reduce(operator.or_, or_queries))

    return queryset
