#!/usr/bin/env python
# encoding: utf-8

from rest_framework import viewsets
from django.db.models import Count

from .models import Rating
from .serializers import RatingSerializer
from .permissions import IsOwnerOrReadOnly

from . import serializers
from .models import Recipe
from v1.recipe_groups.models import Cuisine, Course
from v1.common.recipe_search import get_search_results


class RatingViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Ingredients.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_fields = ('recipe', 'recipe__slug', 'author', 'comment', 'rating')


class BrowseRatingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.RatingSerializer

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

        return query.values('rating').annotate(total=Count('id', distinct=True)).order_by('-rating')
