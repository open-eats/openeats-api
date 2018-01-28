#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from graphene import ObjectType, Field, Schema
from graphene_django.debug import DjangoDebug
from v1.recipe.schema import RecipeQuery, RecipeMutations
from v1.recipe_groups.schema import RecipeGroupQuery, RecipeGroupMutations
from v1.ingredient.schema import IngredientQuery, IngredientMutations
from v1.list.schema import ListQuery, ListMutations


# GraphQl implementation
# TODO: all our this queries are not 100% ready.
# There is a bare bones struture ready to go.
# When the frontend is getting refractored,
# we will switch everything over to GraphQl

class Query(
    RecipeQuery,
    RecipeGroupQuery,
    IngredientQuery,
    ListQuery,
    ObjectType,
):
    if settings.DEBUG:
        debug = Field(DjangoDebug, name='__debug')


class Mutation(
    # RecipeMutations,
    # RecipeGroupMutations,
    # IngredientMutations,
    ListMutations,
    ObjectType
):
    if settings.DEBUG:
        debug = Field(DjangoDebug, name='__debug')

schema = Schema(query=Query, mutation=Mutation)

