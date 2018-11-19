#!/usr/bin/env python
# encoding: utf-8

from django.db.models import Count
from rest_framework import permissions
from rest_framework import viewsets
from django.db.models import Avg

from v1.recipe_groups.models import Cuisine, Course, Tag
from v1.recipe.models import Recipe
from v1.recipe_groups import serializers
from v1.common.permissions import IsOwnerOrReadOnly
from v1.common.recipe_search import get_search_results
from v1.rating.average_rating import convert_rating_to_int


class CuisineViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `title` as the PK for any lookups.
    """
    queryset = Cuisine.objects.all()
    serializer_class = serializers.CuisineSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    lookup_field = 'slug'


class CuisineCountViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `title` as the PK for any lookups.
    """
    serializer_class = serializers.AggCuisineSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    lookup_field = 'slug'

    def get_queryset(self):
        query = Recipe.objects
        filter_set = {}

        # If user is anonymous, restrict recipes to public.
        if not self.request.user.is_authenticated:
            filter_set['public'] = True

        if 'course' in self.request.query_params:
            try:
                filter_set['course__in'] = Course.objects.filter(
                    slug__in=self.request.query_params.get('course').split(',')
                )
            except:
                return []

        if 'search' in self.request.query_params:
            query = get_search_results(
                ['title', 'ingredient_groups__ingredients__title', 'tags__title'],
                query,
                self.request.query_params.get('search')
            ).distinct()

        query = query.filter(**filter_set)
        if 'rating' in self.request.query_params:
            # TODO: this many not be very efficient on huge query sets.
            # I don't think I will ever get to the point of this mattering
            query = query.annotate(rating_avg=Avg('rating__rating'))
            query = [
                recipe.id for recipe in query
                if str(convert_rating_to_int(recipe.rating_avg)) in self.request.query_params.get('rating').split(',')
            ]

        return Cuisine.objects.filter(recipe__in=query).annotate(total=Count('recipe', distinct=True))


class CourseViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `title` as the PK for any lookups.
    """
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    lookup_field = 'slug'


class CourseCountViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `title` as the PK for any lookups.
    """
    serializer_class = serializers.AggCourseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    lookup_field = 'slug'

    def get_queryset(self):
        query = Recipe.objects
        filter_set = {}

        # If user is anonymous, restrict recipes to public.
        if not self.request.user.is_authenticated:
            filter_set['public'] = True

        if 'cuisine' in self.request.query_params:
            try:
                filter_set['cuisine__in'] = Cuisine.objects.filter(
                    slug__in=self.request.query_params.get('cuisine').split(',')
                )
            except:
                return []

        if 'search' in self.request.query_params:
            query = get_search_results(
                ['title', 'ingredient_groups__ingredients__title', 'tags__title'],
                query,
                self.request.query_params.get('search')
            ).distinct()

        query = query.filter(**filter_set)
        if 'rating' in self.request.query_params:
            # TODO: this many not be very efficient on huge query sets.
            # I don't think I will ever get to the point of this mattering
            query = query.annotate(rating_avg=Avg('rating__rating'))
            query = [
                recipe.id for recipe in query
                if str(convert_rating_to_int(recipe.rating_avg)) in self.request.query_params.get('rating').split(',')
            ]

        return Course.objects.filter(recipe__in=query).annotate(total=Count('recipe', distinct=True))


class TagViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `title` as the PK for any lookups.
    """
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    lookup_field = 'title'
