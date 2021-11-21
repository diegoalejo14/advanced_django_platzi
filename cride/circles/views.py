"""Circles views."""

# Django Rest Framework
from cride.circles.serializers import CircleSerializer, CreateCircleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

#from django.http import JsonResponse
from cride.circles.models.circles import Circle
from cride.circles.serializers import CircleSerializer


@api_view(['GET'])
def list_circles(request):
    """List circles"""
    circles = Circle.objects.filter(is_public=True)
    serializer = CircleSerializer(circles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_circle(request):
    """Create circle"""
    serializer=CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # name = request.data['name']
    # slug_name = request.data['slug_name']
    # about = request.data.get('about', '')
    circle = Circle.objects.create(**serializer.data)
    return Response(CircleSerializer(circle).data)
