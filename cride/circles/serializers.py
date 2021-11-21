"""Circle Serializer"""

# Django
from rest_framework import serializers


#

class CircleSerializer(serializers.Serializer):
    """Circle Serializer"""
    name = serializers.CharField()
    slug_name = serializers.CharField()
    about = serializers.CharField()
    rides_taken = serializers.IntegerField()
    rides_offered = serializers.IntegerField()
    members_limit = serializers.IntegerField()


class CreateCircleSerializer(serializers.Serializer):
    """Create Circle Serializer"""
    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(max_length=40)
    about = serializers.CharField(max_length=255, required=False)
