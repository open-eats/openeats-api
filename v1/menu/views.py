#!/usr/bin/env python
# encoding: utf-8

from rest_framework import permissions, viewsets

from .models import MenuItem, Menu
from .serializers import MenuItemSerializer, MenuSerializer
from v1.common.permissions import IsOwnerOrReadOnly


class MenuItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Ingredients.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # IsOwnerOrReadOnly
    )
    # filter_fields = ('recipe',)


class MenuViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Ingredients.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # IsOwnerOrReadOnly
    )
    # filter_fields = ('ingredient_group', 'ingredient_group__recipe')
