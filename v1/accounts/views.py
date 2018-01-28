#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        """ Tests if a users is authentication if they supply pk == 'i' """
        if pk == 'i':
            return Response(UserSerializer(request.user, context={'request':request}).data)
        return super(UserViewSet, self).retrieve(request, pk)

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'id': user.id, 'token': token.key})

custom_obtain_auth_token = CustomObtainAuthToken.as_view()