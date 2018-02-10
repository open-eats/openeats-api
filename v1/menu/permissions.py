#!/usr/bin/env python
# encoding: utf-8

from rest_framework import permissions


class IsMenuOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners
    of an list and admins to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Only show all data to super admins.
        if request.user.is_superuser:
            return True

        # Write permissions are only allowed to the owner of the list.
        return obj.author == request.user


class IsMenuItemOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners
    of an item and admins to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Only show all data to super admins.
        if request.user.is_superuser:
            return True

        # Write/Read permissions are only allowed to the owner of the list.
        return obj.menu.author == request.user
