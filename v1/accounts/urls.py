#!/usr/bin/env python
# encoding: utf-8

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('obtain-auth-token/', obtain_jwt_token),
    path('refresh-auth-token/', refresh_jwt_token)
]
