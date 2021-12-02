"""Rides views."""

# Django REST Framework
from cride.rides import serializers
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
# Serializers
from cride.rides.serializers import CreateRideSerializer, RideModelSerializer, JoinRideModelSerializer

# Models
from cride.circles.models import Circle


# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember
from cride.rides.permissions.rides import IsRideOwner

# Utilities
from datetime import timedelta
from django.utils import timezone

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter


class RidesViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet
                   ):
    """Rides view set."""

    serializer_class = CreateRideSerializer
    permission_classes = [IsAuthenticated, IsActiveCircleMember]

    # Filters
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('departure_location', 'arrival_location')
    ordering_fields = ('departure_date', 'arrival_date', 'available_seats')
    ordering = ('departure_date', 'arrival_date', 'available_seats')

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists."""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(
            Circle,
            slug_name=slug_name
        )
        return super(RidesViewSet, self).dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        """Add circle to serializer context."""
        context = super(RidesViewSet, self).get_serializer_context()
        context['circle'] = self.circle
        return context

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create':
            return CreateRideSerializer
        if self.action == 'join':
            return JoinRideModelSerializer
        else:
            return RideModelSerializer

    def get_queryset(self):
        """Return active circle's rides"""
        offset = timezone.now() - timedelta(minutes=10)
        return self.circle.ride_set.filter(
            departure_date__gte=offset,
            is_active=True,
            available_seats__gte=1
        )

    def get_permissions(self):
        """Assign permission base on action"""
        permissions = [IsAuthenticated, IsActiveCircleMember]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsRideOwner)
        return [p() for p in permissions]

    @action(detail=True, methods=['post'])
    def join(self, request, *args, **kwargs):
        """Join a user to a ride"""
        ride = self.get_object()
        serializer_class =self.get_serializer_class()
        serializer=serializer_class(
            ride,
            data={'passenger': request.user.pk},
            context={'ride': ride, 'circle': self.circle},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        ride=serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)
