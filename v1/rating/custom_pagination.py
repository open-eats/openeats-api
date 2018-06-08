#!/usr/bin/env python
# encoding: utf-8

from functools import reduce
from rest_framework.pagination import LimitOffsetPagination
from collections import OrderedDict
from rest_framework.response import Response

from .models import Rating


class RatingPagination(LimitOffsetPagination):

    def get_average_rating(self):
        if 'recipe' in self.request.query_params:
            ratings = Rating.objects.filter(
                recipe_id=self.request.query_params.get('recipe')
            )
            if len(ratings) < 1:
                return 0
        else:
            ratings = Rating.objects.all()
        return reduce((lambda x, y: x + y), [r.rating for r in ratings]) / len(ratings)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('rating', self.get_average_rating()),
            ('results', data)
        ]))
