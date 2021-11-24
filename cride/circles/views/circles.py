"""Circles view."""

#Django Rest Framework

from rest_framework import viewsets


#Serializer
from cride.circles.serializers import CircleModelSerializer

#Models
from cride.circles.models import Circle


class CircleViewSet(viewsets.ModelViewSet):
  """Circle View set"""
  queryset=Circle.objects().all()
  serializer_class=CircleModelSerializer
