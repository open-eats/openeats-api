#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
import graphene

from v1.common.total_count import total_count
from v1.common.deletion import DeleteModel, DeleteMutation, BulkDeleteModel
from .models import GroceryList, GroceryItem


class GroceryListNode(DjangoObjectType):
    class Meta:
        model = GroceryList
        interfaces = (graphene.relay.Node, )

    @classmethod
    def get_node(cls, id, context, info):
        try:
            glist = cls._meta.model.objects.get(id=id)
        except cls._meta.model.DoesNotExist:
            return None

        if context.user == glist.author:
            return glist
        return None


class GroceryItemNode(DjangoObjectType):
    class Meta:
        model = GroceryItem
        filter_fields = ['slug', 'list__id']
        interfaces = (graphene.relay.Node, )

    @classmethod
    def get_node(cls, id, context, info):
        try:
            item = cls._meta.model.objects.get(id=id)
        except cls._meta.model.DoesNotExist:
            return None

        if context.user == item.list.author:
            return item
        return None

GroceryItemNode.Connection = total_count(GroceryItemNode)


class ListQuery(graphene.AbstractType):
    grocery_list = graphene.Node.Field(GroceryListNode)
    all_grocery_lists = DjangoFilterConnectionField(GroceryListNode)
    grocery_item = graphene.relay.Node.Field(GroceryItemNode)
    all_grocery_items = DjangoFilterConnectionField(GroceryItemNode)

    def resolve_all_grocery_lists(self, args, context, info):
        if not context.user.is_authenticated():
            return GroceryList.objects.none()
        else:
            return GroceryList.objects.filter(author=context.user)

    def resolve_all_grocery_items(self, args, context, info):
        if not context.user.is_authenticated():
            return GroceryItem.objects.none()
        else:
            return GroceryItem.objects.filter(list__author=context.user)


class GroceryListInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()


class CreateGroceryList(graphene.Mutation):
    class Input:
        data = graphene.Argument(GroceryListInput)

    grocery_list = graphene.Field(lambda: GroceryListNode)

    @staticmethod
    def mutate(root, args, context, info, model=None):
        if context.user.is_authenticated():
            title = args.get('data').get('title')
            grocery_list = GroceryList.objects.create(title=title, author_id=context.user)
            grocery_list.save()
            return CreateGroceryList(grocery_list=grocery_list)


class UpdateGroceryList(graphene.Mutation):
    class Input:
        data = graphene.Argument(GroceryListInput)

    grocery_list = graphene.Field(lambda: GroceryListNode)

    @staticmethod
    def mutate(root, args, context, info, model=None):
        if context.user.is_authenticated():
            key = args.get('data').get('id')
            grocery_list = GroceryList.objects.get(id=key)
            if grocery_list.user == context.user:
                title = args.get('data').get('title')
                grocery_list.title = title
                grocery_list.save()
            return UpdateGroceryList(grocery_list=grocery_list)


class DeleteGroceryList(DeleteModel, DeleteMutation):
    class Config:
        model = GroceryList
        auth = 'author'


class BulkDeleteGroceryList(BulkDeleteModel, DeleteMutation):
    class Config:
        model = GroceryList
        auth = 'author'


class GroceryItemInput(graphene.InputObjectType):
    id = graphene.ID()
    list = graphene.ID()
    title = graphene.String()
    completed = graphene.Boolean()


class CreateGroceryItem(graphene.Mutation):
    class Input:
        data = graphene.Argument(GroceryItemInput)

    grocery_item = graphene.Field(lambda: GroceryItemNode)

    @staticmethod
    def mutate(root, args, context, info, model=None):
        list_id = args.get('data').get('list')
        title = args.get('data').get('title')
        grocery_item = GroceryItem.objects.create(title=title, list_id=list_id)
        grocery_item.save()
        return CreateGroceryItem(grocery_item=grocery_item)


class UpdateGroceryItem(graphene.Mutation):
    class Input:
        data = graphene.Argument(GroceryItemInput)

    grocery_item = graphene.Field(lambda: GroceryItemNode)

    @staticmethod
    def mutate(root, args, context, info, model=None):
        if context.user.is_authenticated():
            key = args.get('data').get('id')
            grocery_item = GroceryItem.objects.get(id=key)
            if grocery_item.list.user == context.user:
                list_id = args.get('data').get('list')
                title = args.get('data').get('title')
                completed = args.get('data').get('completed')
                if list_id:
                    grocery_item.list_id = list_id
                if title:
                    grocery_item.title = title
                if completed is not None:
                    grocery_item.completed = completed
                grocery_item.save()
                return UpdateGroceryItem(grocery_item=grocery_item)


class DeleteGroceryItem(DeleteModel, DeleteMutation):
    class Config:
        model = GroceryItem
        auth = 'list__author'


class BulkDeleteGroceryItem(BulkDeleteModel, DeleteMutation):
    class Config:
        model = GroceryItem
        auth = 'list__author'


class ListMutations(graphene.AbstractType):
    create_grocery_list = CreateGroceryList.Field()
    update_grocery_list = UpdateGroceryList.Field()
    delete_grocery_list = DeleteGroceryList.Field()
    bulk_delete_grocery_list = BulkDeleteGroceryList.Field()
    create_grocery_item = CreateGroceryItem.Field()
    update_grocery_item = UpdateGroceryItem.Field()
    delete_grocery_item = DeleteGroceryItem.Field()
    bulk_delete_grocery_item = BulkDeleteGroceryItem.Field()
