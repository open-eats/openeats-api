#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
import graphene

from v1.common.deletion import DeleteModel, DeleteMutation, BulkDeleteModel
from .models import Ingredient, IngredientGroup


class IngredientGroupNode(DjangoObjectType):
    class Meta:
        model = IngredientGroup
        interfaces = (graphene.relay.Node, )
        filter_fields = ['id', 'title']


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        interfaces = (graphene.relay.Node, )
        filter_fields = ['id', 'title']


class IngredientQuery(graphene.AbstractType):
    ingredient_group = graphene.relay.Node.Field(IngredientGroupNode)
    all_ingredient_groups = DjangoFilterConnectionField(IngredientGroupNode)
    ingredient = graphene.relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)


class IngredientGroupInput(graphene.InputObjectType):
    id = graphene.ID()
    recipe = graphene.ID()
    title = graphene.String()


class CreateIngredientGroup(graphene.Mutation):
    class Input:
        data = graphene.Argument(IngredientGroupInput)

    ingredient_group = graphene.Field(lambda: IngredientGroupNode)

    @staticmethod
    def mutate(root, args, context, info, model=None):
        recipe = args.get('data').get('recipe')
        title = args.get('data').get('title')
        ingredient_group = IngredientGroup.objects.create(title=title, recipe=recipe)
        ingredient_group.save()
        return CreateIngredientGroup(ingredient_group=ingredient_group)


class UpdateIngredientGroup(graphene.Mutation):
    class Input:
        data = graphene.Argument(IngredientGroupInput)

    ingredient_group = graphene.Field(lambda: IngredientGroupNode)

    @staticmethod
    def mutate(root, args, context, info, model=None):
        key = args.get('data').get('id')
        title = args.get('data').get('title')
        ingredient_group = IngredientGroup.objects.get(id=key)
        ingredient_group.title = title
        ingredient_group.save()
        return UpdateIngredientGroup(ingredient_group=ingredient_group)


class DeleteIngredientGroup(DeleteModel, DeleteMutation):
    class Config:
        model = IngredientGroup


class BulkDeleteIngredientGroup(BulkDeleteModel, DeleteMutation):
    class Config:
        model = IngredientGroup


class IngredientInput(graphene.InputObjectType):
    id = graphene.ID()
    ingredient_group = graphene.ID()
    title = graphene.String()
    quantity = graphene.Float()
    measurement = graphene.String()


class CreateIngredient(graphene.Mutation):
    class Input:
        data = graphene.Argument(IngredientInput)

    ingredient = graphene.Field(lambda: IngredientNode)

    @staticmethod
    def mutate(root, args, context, info, model=None):
        ingredient_group = args.get('data').get('ingredient_group')
        title = args.get('data').get('title')
        quantity = args.get('data').get('quantity')
        measurement = args.get('data').get('measurement')
        ingredient = Ingredient.objects.create(title=title, ingredient_group=ingredient_group)
        if quantity:
            ingredient.quantity = quantity
        if measurement:
            ingredient.measurement = measurement
        ingredient.save()
        return CreateIngredient(ingredient=ingredient)


class UpdateIngredient(graphene.Mutation):
    class Input:
        data = graphene.Argument(IngredientInput)

    ingredient = graphene.Field(lambda: IngredientNode)

    @staticmethod
    def mutate(root, args, context, info, model=None):
        key = args.get('data').get('id')
        ingredient_group = args.get('data').get('ingredient_group')
        title = args.get('data').get('title')
        quantity = args.get('data').get('quantity')
        measurement = args.get('data').get('measurement')
        ingredient = Ingredient.objects.get(id=key)
        if ingredient_group:
            ingredient.ingredient_group = ingredient_group
        if title:
            ingredient.title = title
        if quantity:
            ingredient.quantity = quantity
        if measurement:
            ingredient.measurement = measurement
        ingredient.save()
        return UpdateIngredient(ingredient=ingredient)


class DeleteIngredient(DeleteModel, DeleteMutation):
    class Config:
        model = Ingredient


class BulkDeleteIngredient(BulkDeleteModel, DeleteMutation):
    class Config:
        model = Ingredient


class IngredientMutations(graphene.AbstractType):
    create_ingredient_group = CreateIngredientGroup.Field()
    update_ingredient_group = UpdateIngredientGroup.Field()
    delete_ingredient_group = DeleteIngredientGroup.Field()
    bulk_delete_ingredient_group = BulkDeleteIngredientGroup.Field()
    create_ingredient = CreateIngredient.Field()
    update_ingredient = UpdateIngredient.Field()
    delete_ingredient = DeleteIngredient.Field()
    bulk_delete_ingredient = BulkDeleteIngredient.Field()
