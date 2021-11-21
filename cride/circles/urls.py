from django.urls.resolvers import URLPattern


"""Circles URLS."""

from django.urls import path
#Views
from cride.circles.views import list_circles,create_circle

urlpatterns=[
  path('circles/',list_circles),
  path('circles/create',create_circle)
]