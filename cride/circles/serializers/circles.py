"""Circle Serializers"""

# Django framework
from rest_framework import serializers


# Model
from circles.models import Circle


class CircleModelSerializer(serializers.ModelSerialiazer):
    """Circle model serializaer"""

    class Meta:
        model = Circle
        fields = (
            'id', 'name', 'slug_name',
            'about', 'picture',
            'rides_offered', 'rides_taken',
            'verified', 'is_public',
            'is_limited', 'members_limit'

        )
