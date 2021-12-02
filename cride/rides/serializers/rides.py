"""Rides serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from cride.rides.models.rides import Ride
from cride.circles.models import Membership
from cride.users.models import User


# Utilities
from datetime import timedelta
from django.utils import timezone


# Serializers
from cride.users.serializers.users import UserModelSerializer


class CreateRideSerializer(serializers.ModelSerializer):
    """Create Ride serializer"""
    offered_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    available_seats = serializers.IntegerField(min_value=1, max_value=15)

    class Meta:
        """Meta class."""
        model = Ride
        exclude = ('offered_in', 'passengers', 'rating', 'is_active')

    def validate_departure_date(self, data):
        """Verify if date is not in the pass"""
        min_date = timezone.now()+timedelta(minutes=10)
        if data < min_date:
            raise serializers.ValidationError(
                'Departure time must be at least passing the next 20 minutes window.'
            )
        return data

    def validate(self, data):
        """
        Verify that the person who offers the ride is member and also the same user making the request
        """
        user = data['offered_by']
        circle = self.context['circle']
        try:
            membership = Membership.objects.get(
                user=user,
                circle=circle,
                is_active=True)
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle')
        if self.context['request'].user != user:
            raise serializers.ValidationError('Rides offered on behalf others are not allowed.')
        if data['arrival_date'] <= data['departure_date']:
            raise serializers.ValidationError('Departure data must happen after arrival date')
        self.context['membership'] = membership
        return data

    def create(self, data):
        """Create ride and update stats."""
        circle = self.context['circle']
        ride = Ride.objects.create(**data, offered_in=circle)
        # Circle
        circle.rides_offered += 1
        circle.save()

        # Membership
        membership = self.context['membership']
        membership.rides_offered += 1
        membership.save()
        # Profile
        profile = data['offered_by'].profile
        profile.rides_offered += 1
        profile.save()
        return ride


class RideModelSerializer(serializers.ModelSerializer):
    """Ride model serializer."""

    offered_by = UserModelSerializer(read_only=True)
    offered_in = serializers.StringRelatedField()

    passengers = UserModelSerializer(read_only=True, many=True)

    class Meta:
        """Meta class."""
        model = Ride
        fields = '__all__'
        read_only_fields = (
            'offered_by',
            'offered_in'
            'rating'
        )

    def update(self, instance, validationData):
        """Allow updates only beofre dearture date."""
        now = timezone.now()
        if instance.departure_date <= now:
            raise serializers.ValidationError('Ongoing cannot be modified')
        return super(RideModelSerializer, self).update(instance, validationData)


class JoinRideModelSerializer(serializers.ModelSerializer):
    """Join model serializer."""

    passenger = serializers.IntegerField()

    class Meta:
        """Meta class."""
        model = Ride
        fields = ('passenger',)

    def validate_passenger(self, data):
        """Verify passenger exist and is a circle member."""
        try:
            user = User.objects.get(pk=data)
        except User.DoesNotxist:
            raise serializers.ValidationError('Invalid passenger')
        circle = self.context['circle']
        try:
            member = Membership.objects.get(user=user, circle=circle, is_active=True)
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle')
        self.context['member'] = member
        self.context['user'] = user
        return data

    def validate(self, data):
        """Verify rides allow new passenger"""
        ride = self.context['ride']
        if ride.departure_date <= timezone.now():
            raise serializers.ValidationError('You cannot join this ride now')
        if ride.available_seats < 1:
            raise serializers.ValidationError('Ride is already full')
        if ride.passengers.filter(pk=self.context['user'].pk).exists():
            raise serializers.ValidationError('Passenger is already in this trip')
        
        return data

    def update(self, instance, data):
        """Add passenger to ride and update stats."""
        ride = self.context['ride']
        circle = self.context['circle']
        user = self.context['user']
        ride.passengers.add(user)
        # Profile
        profile = user.profile
        profile.rides_taken += 1
        profile.save()
        # Membership
        member = self.context['member']
        member.rides_taken += 1
        member.save()
        # Circle
        circle.rides_taken += 1
        circle.save()

        return ride
