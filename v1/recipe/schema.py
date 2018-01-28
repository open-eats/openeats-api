#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
import graphene

from v1.common.deletion import DeleteModel, DeleteMutation
from v1.common.total_count import total_count
from v1.common.list_scalar import List
from .models import Recipe, SubRecipe


class RecipeNode(DjangoObjectType):
    class Meta:
        model = Recipe
        interfaces = (graphene.relay.Node, )
        filter_fields = ['id', 'title']

RecipeNode.Connection = total_count(RecipeNode)


class SubRecipeNode(DjangoObjectType):
    class Meta:
        model = SubRecipe
        interfaces = (graphene.relay.Node, )


class RecipeQuery(graphene.AbstractType):
    sub_recipe = graphene.relay.Node.Field(SubRecipeNode)
    all_sub_recipes = DjangoFilterConnectionField(SubRecipeNode)
    recipe = graphene.relay.Node.Field(RecipeNode)
    all_recipes = DjangoFilterConnectionField(RecipeNode)


class SubRecipeInput(graphene.InputObjectType):
    id = graphene.ID()
    child_recipe = graphene.ID()
    parent_recipe = graphene.ID()
    quantity = graphene.Float()
    measurement = graphene.String()


class RecipeInput(graphene.InputObjectType):
    id = graphene.ID()
    course = graphene.ID()
    cuisine = graphene.ID()
    title = graphene.String()
    info = graphene.String()
    source = graphene.String()
    prep_time = graphene.Int()
    cook_time = graphene.Int()
    servings = graphene.Int()
    rating = graphene.Int()
    direction = graphene.String()
    sub_recipes = graphene.Argument(SubRecipeInput)
    tags = List()


class CreateRecipe(graphene.Mutation):
    class Input:
        # author
        # photo
        data = graphene.Argument(RecipeInput)

    recipe = graphene.Field(lambda: RecipeNode)

    @staticmethod
    def mutate(root, args, context, info):
        photo = context.FILES.get('photo')

        title = args.get('data').get('title')
        info = args.get('data').get('info')
        source = args.get('data').get('source')
        prep_time = args.get('data').get('prep_time')
        cook_time = args.get('data').get('cook_time')
        servings = args.get('data').get('servings')
        rating = args.get('data').get('rating')

        recipe = Recipe.objects.create(
            title=title,
            info=info,
            source=source,
            prep_time=prep_time,
            cook_time=cook_time,
            servings=servings,
            rating=rating,
            cuisine_id=1,
            course_id=1,
        )
        if photo:
            recipe.photo = photo
        recipe.save()
        return CreateRecipe(recipe=recipe)


class RecipeMutations(graphene.AbstractType):
    create_recipe = CreateRecipe.Field()
