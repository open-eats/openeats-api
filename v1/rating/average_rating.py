#!/usr/bin/env python
# encoding: utf-8

from functools import reduce
from .models import Rating


def convert_rating_to_int(rating):
    if not rating:
        return 0
    rating = int(rating)
    rating = 5 if rating > 5 else rating
    rating = 0 if rating < 0 else rating
    return rating


def average_rating(recipe_id):
    # TODO: this many not be very efficient on huge query sets.
    # I don't think I will ever get to the point of this mattering
    ratings = Rating.objects.filter(recipe_id=recipe_id)
    if len(ratings) < 1:
        return 0
    return convert_rating_to_int(
        reduce((lambda x, y: x + y), [r.rating for r in ratings]) / len(ratings)
    )
