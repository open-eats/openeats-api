#!/usr/bin/env python
# encoding: utf-8

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta
from dateutil import parser

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
    filter_fields = ('title', 'author',)


class MenuItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Menu Items.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (IsMenuItemOwner,)
    filter_fields = ('menu', 'recipe', 'start_date', 'end_date')


class MenuCopyViewSet(APIView):
    def post(self, request, *args, **kwargs):
        menu = request.data.get('menu')
        title = request.data.get('title')
        description = request.data.get('description')
        start = request.data.get('start')

        new_menu = MenuSerializer(data={
            'title': title,
            'description': description
        })
        new_menu.is_valid(raise_exception=True)
        new_menu.save()

        first_item = MenuItem.objects.filter(
            menu__id=menu
        ).order_by(
            'start_date'
        ).first()
        days = (parser.parse(start) - first_item.start_date).days

        new_items = []
        for item in MenuItem.objects.filter(menu__id=menu):
            new_item = MenuItemSerializer(data={
                'menu': new_menu.data.get('id'),
                'recipe': item.recipe.id,
                'all_day': item.all_day,
                'start_date': item.start_date + timedelta(days=days),
                'end_date': item.end_date + timedelta(days=days)
            })
            new_item.is_valid(raise_exception=True)
            new_item.save()
            new_items.append(new_item.data)

        return Response({'menu': new_menu.data, 'items': new_items})
