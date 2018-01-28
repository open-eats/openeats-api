#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
from rest_framework import permissions, filters, viewsets, status
from rest_framework.response import Response
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

from .models import GroceryList, GroceryItem
from .serializers import GroceryListSerializer, \
    GroceryItemSerializer, BulkGroceryItemSerializer
from .permissions import IsListOwner, IsItemOwner


class GroceryListViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = GroceryListSerializer
    permission_classes = (IsListOwner,)

    def get_queryset(self):
        user = self.request.user
        if user and not user.is_anonymous:
            return GroceryList.objects.filter(author=user)
        return GroceryList.objects.none()


class GroceryItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Allows filtering by GroceryList `list={list_id}`
    """
    serializer_class = GroceryItemSerializer
    permission_classes = (IsItemOwner,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('list',)

    def get_queryset(self):
        user = self.request.user
        if user and not user.is_anonymous:
            return GroceryItem.objects.filter(list__author=user).order_by('list')
        return GroceryItem.objects.none()


class BulkGroceryItemViewSet(ListBulkCreateUpdateDestroyAPIView):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions in bulk.
    See: https://github.com/miki725/django-rest-framework-bulk
    """
    queryset = GroceryItem.objects.all()
    serializer_class = BulkGroceryItemSerializer
    permission_classes = (IsItemOwner,)

    def bulk_destroy(self, request, *args, **kwargs):
        qs = self.get_queryset()

        filtered = qs.filter(id__in=self.request.data)
        if not self.allow_bulk_destroy(qs, filtered):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        self.perform_bulk_destroy(filtered)

        return Response(status=status.HTTP_204_NO_CONTENT)
