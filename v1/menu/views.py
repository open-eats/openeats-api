#!/usr/bin/env python
# encoding: utf-8

from rest_framework import viewsets

from .models import MenuItem, Menu
from .serializers import MenuItemSerializer, MenuSerializer
from .permissions import IsMenuOwner, IsMenuItemOwner


class MenuViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Menus.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsMenuOwner,)
    filter_fields = ('start_date', 'end_date', 'author')


class MenuItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Menu Items.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (IsMenuItemOwner,)
    filter_fields = ('menu', 'recipe', 'start_date', 'end_date')
