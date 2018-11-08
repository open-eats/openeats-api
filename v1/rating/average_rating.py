#!/usr/bin/env python
# encoding: utf-8

from functools import reduce
from .models import Rating


def average_rating(recipe_id):
    ratings = Rating.objects.filter(recipe_id=recipe_id)
    if len(ratings) < 1:
        return 0
    return reduce((lambda x, y: x + y), [r.rating for r in ratings]) / len(ratings)
