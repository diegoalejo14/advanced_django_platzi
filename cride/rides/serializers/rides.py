"""Rides serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from cride.rides.models.rides import Ride
from cride.circles.models import Membership


# Utilities
from datetime import timedelta
from django.utils import timezone


#Serializers
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
    
    offered_by=UserModelSerializer(read_only=True)
    offered_in=serializers.StringRelatedField()

    passengers=UserModelSerializer(read_only=True,many=True)

    class Meta:
        """Meta class."""
        model = Ride
        fields='__all__'
        read_only_fields=(
            'offered_by',
            'offered_in'
            'rating'
        )
    

    def update(self,instance,validationData):
        """Allow updates only beofre dearture date."""
        now=timezone.now()
        if instance.departure_date<=now:
            raise serializers.ValidationError('Ongoing cannot be modified')
        return super(RideModelSerializer,self).update(instance,validationData)

