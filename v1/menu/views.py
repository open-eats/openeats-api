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
    filter_fields = ('recipe', 'start_date', 'end_date', 'complete')

    def get_queryset(self):
        user = self.request.user
        if user and not user.is_anonymous:
            return MenuItem.objects.filter(author=user)
        return MenuItem.objects.none()