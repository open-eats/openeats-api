#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.settings import api_settings
from rest_framework.request import Request
from graphene_django.views import GraphQLView


class DRFAuthenticatedGraphQLView(GraphQLView):
    def parse_body(self, request):
        if isinstance(request, Request):
            return request.data
        return super(GraphQLView, self).parse_body(request)

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(GraphQLView, cls).as_view(*args, **kwargs)
        view = permission_classes((IsAuthenticated,))(view)
        view = authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES)(view)
        view = api_view(['GET', 'POST'])(view)
        return view


admin.autodiscover()

urlpatterns = [
    # Backend REST API
    url(r'^api/v1/', include('v1.urls', namespace='v1')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # GraphQL
    url(r'^graphql', csrf_exempt(DRFAuthenticatedGraphQLView.as_view())),

    # Generic Static Home
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),

    # Admin
    url(r'^admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [url(r'^graphiql/', csrf_exempt(GraphQLView.as_view(graphiql=True)))]
