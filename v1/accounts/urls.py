#!/usr/bin/env python
# encoding: utf-8

from django.urls import path
from v1.accounts.views import custom_obtain_auth_token

urlpatterns = [path('obtain-auth-token/', custom_obtain_auth_token)]
