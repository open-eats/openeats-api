#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
import graphene

from v1.common.deletion import DeleteModel, DeleteMutation
from .models import Tag, Course, Cuisine


class TagNode(DjangoObjectType):
    class Meta:
        model = Tag
        interfaces = (graphene.relay.Node, )
        filter_fields = ['id', 'title']


class CourseNode(DjangoObjectType):
    class Meta:
        model = Course
        interfaces = (graphene.relay.Node, )
        filter_fields = ['id', 'title']


class CuisineNode(DjangoObjectType):
    class Meta:
        model = Cuisine
        interfaces = (graphene.relay.Node, )
        filter_fields = ['id', 'title']


class RecipeGroupQuery(graphene.AbstractType):
    cuisine = graphene.relay.Node.Field(CuisineNode)
    all_cuisines = DjangoFilterConnectionField(CuisineNode)
    course = graphene.relay.Node.Field(CourseNode)
    all_courses = DjangoFilterConnectionField(CourseNode)
    tag = graphene.relay.Node.Field(TagNode)
    all_tags = DjangoFilterConnectionField(TagNode)


class GroceryCuisineInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()


class CreateCuisine(graphene.Mutation):
    class Input:
        data = graphene.Argument(GroceryCuisineInput)

    cuisine = graphene.Field(lambda: CuisineNode)

    @staticmethod
    def mutate(root, args, context, info):
        title = args.get('data').get('title')
        cuisine = Cuisine.objects.create(title=title)
        cuisine.save()
        return CreateCuisine(cuisine=cuisine)


class UpdateCuisine(graphene.Mutation):
    class Input:
        data = graphene.Argument(GroceryCuisineInput)

    cuisine = graphene.Field(lambda: CuisineNode)

    @staticmethod
    def mutate(root, args, context, info):
        key = args.get('data').get('id')
        title = args.get('data').get('title')
        cuisine = Cuisine.objects.get_or_create(id=key)
        if title:
            cuisine.title = title
        cuisine.save()
        return UpdateCuisine(cuisine=cuisine)


class DeleteCuisine(DeleteModel, DeleteMutation):
    class Config:
        model = Cuisine


class GroceryCourseInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()


class CreateCourse(graphene.Mutation):
    class Input:
        data = graphene.Argument(GroceryCuisineInput)

    course = graphene.Field(lambda: CourseNode)

    @staticmethod
    def mutate(root, args, context, info):
        title = args.get('data').get('title')
        course = Course.objects.create(title=title)
        course.save()
        return CreateCourse(course=course)


class UpdateCourse(graphene.Mutation):
    class Input:
        data = graphene.Argument(GroceryCuisineInput)

    course = graphene.Field(lambda: CourseNode)

    @staticmethod
    def mutate(root, args, context, info):
        key = args.get('data').get('id')
        title = args.get('data').get('title')
        course = Course.objects.get_or_create(id=key)
        if title:
            course.title = title
        course.save()
        return UpdateCourse(course=course)


class DeleteCourse(DeleteModel, DeleteMutation):
    class Config:
        model = Course


class RecipeGroupMutations(graphene.AbstractType):
    create_cuisine = CreateCuisine.Field()
    update_cuisine = UpdateCuisine.Field()
    delete_cuisine = DeleteCuisine.Field()
    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()
    delete_course = DeleteCourse.Field()
