#!/usr/bin/env python
# encoding: utf-8

from rest_framework import viewsets

from .models import MenuItem
from .serializers import MenuItemSerializer
from .permissions import IsMenuItemOwner


class MenuItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Menu Items.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (IsMenuItemOwner,)
    filter_fields = ('recipe', 'start_date', 'end_date')

    # def get_queryset(self):
    #     if self.request.user:
    #         return MenuItem.objects.filter(author=self.request.user)
    #     return MenuItem.objects.all()