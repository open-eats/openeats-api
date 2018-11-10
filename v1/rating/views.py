#!/usr/bin/env python
# encoding: utf-8

from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.views import APIView

from rest_framework.response import Response

from .models import Rating
from .serializers import RatingSerializer
from .permissions import IsOwnerOrReadOnly

from .models import Recipe
from v1.recipe_groups.models import Cuisine, Course
from v1.common.recipe_search import get_search_results
from v1.rating.average_rating import convert_rating_to_int


class RatingViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Ingredients.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_fields = ('recipe', 'recipe__slug', 'author', 'comment', 'rating')


class RatingCountViewSet(APIView):
    def get(self, request, *args, **kwargs):
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

        results = {
            5: 0,
            4: 0,
            3: 0,
            2: 0,
            1: 0,
            0: 0,
        }
        query = query.filter(**filter_set)
        # TODO: this many not be very efficient on huge query sets.
        # I don't think I will ever get to the point of this mattering
        for x in query.annotate(rating_avg=Avg('rating__rating')):
            results[convert_rating_to_int(x.rating_avg)] += 1

        return Response({
            'results': [{"rating": k, "total": v} for k, v in results.items()]
        })
