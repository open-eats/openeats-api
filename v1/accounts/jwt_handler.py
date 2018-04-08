#!/usr/bin/env python
# encoding: utf-8

from .serializers import UserSerializer


def handler(token, user=None, request=None):
    return {
        'token': token,
        'id': UserSerializer(user, context={'request': request}).data.get('id')
    }
