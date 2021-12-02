"""Rides views."""

# Django REST Framework
from cride.rides import serializers
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
# Serializers
from cride.rides.serializers import CreateRideSerializer, RideModelSerializer, JoinRideModelSerializer, EndRideSerializer
from cride.rides.serializers.ratings import CreateRideRatingSerializer

# Models
from cride.circles.models import Circle


# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember
from cride.rides.permissions.rides import IsRideOwner, IsNotRideOwner

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
        print('==GETSERIALIZER',self.action)        
        """Return serializer based on action."""
        if self.action == 'create':
            return CreateRideSerializer
        if self.action == 'join':
            return JoinRideModelSerializer
        if self.action == 'finish':
            return EndRideSerializer
        if self.action=='rate':
            return CreateRideRatingSerializer
        else:
            return RideModelSerializer

    def get_queryset(self):
        """Return active circle's rides"""
        if self.action != 'finish':
            offset = timezone.now() - timedelta(minutes=10)
            return self.circle.ride_set.filter(
                departure_date__gte=offset,
                is_active=True,
                available_seats__gte=1
            )
        return self.circle.ride_set.all()

    def get_permissions(self):
        """Assign permission base on action"""
        permissions = [IsAuthenticated, IsActiveCircleMember]
        if self.action in ['update', 'partial_update', 'finish']:
            permissions.append(IsRideOwner)
        if self.action == 'join':
            permissions.append(IsNotRideOwner)

        return [p() for p in permissions]

    @action(detail=True, methods=['post'])
    def join(self, request, *args, **kwargs):
        """Join a user to a ride"""
        ride = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            ride,
            data={'passenger': request.user.pk},
            context={'ride': ride, 'circle': self.circle},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def finish(self, request, *args, **kwargs):
        """Finish a ride"""
        ride = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            ride,
            data={
                'is_active': False,
                'current_time': timezone.now()
            },
            context=self.get_serializer_context(),
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def rate(self, request, *args, **kwargs):
        """Rate a Ride"""
        ride = self.get_object()
        serializer_class = self.get_serializer_class()
        print('===CONTEXT',serializer_class)
        context=self.get_serializer_context()
        context['ride']=ride
        serializer = serializer_class(
            data=request.data,
            context=context
        )
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_201_CREATED)
