"""Membership serializers."""

# Django REST Framework
from rest_framework import serializers

# Serializers
from cride.users.serializers.users import UserModelSerializer
# Models
from cride.circles.models import Membership, Invitation
from cride.users.models import User
#Django Utilities
from django.utils import timezone


class MembershipModelSerializer(serializers.ModelSerializer):
    """Member model serializer"""
    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    joined_at = serializers.DateTimeField(source='created', read_only=True)

    class Meta:
        """Meta class."""
        model = Membership
        fields = (
            'user',
            'is_admin',
            'is_active',
            'used_invitations',
            'remaining_invitation',
            'rides_taken',
            'rides_offered',
            'joined_at',
            'invited_by'

        )
        read_only_fields = (
            'user',
            'used_invitations',
            'invited_by'
        )


class AddMemberSerializer(serializers.Serializer):
    """Add member serializer

    Handle the process to add member a circle"""
    invitation_code = serializers.CharField(min_length=8)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, data):
        """Verify user is not a member"""
        circle = self.context['circle']
        user = data
        q = Membership.objects.filter(
            circle=circle,
            user=user
        )
        if q.exists():
            raise serializers.ValidationError('User is already member of this circle.')
        return data 

    def validate_invitation_code(self, data):
        """Verify if code exists and it is related to the circle."""
        try:
            invitation = Invitation.objects.get(
                code=data,
                circle=self.context['circle'],
                used=False
            )
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Invalid Invitation')
        self.context['invitation'] = invitation
        return data

    def validate(self, data):
        """Verify circle could accept a new member"""
        circle = self.context['circle']
        if circle.is_limited and circle.members.count() >= circle.members_limit:
            raise serializers.ValidationError('Circle has reached a member limit')
        return data

    def create(self, data):
        """Add member to circle"""
        circle = self.context['circle']
        invitation = self.context['invitation']
        user=User.objects.filter(username=data['user'])[0]
        now=timezone.now()
        member=Membership.objects.create(
            user=user,
            profile=user.profile,
            circle=circle,
            invited_by=invitation.issued_by
        )
        #Update Invitation
        invitation.used_by=user
        invitation.used=True
        invitation.used_at=now
        invitation.save()
        #Update issuer data
        issuer=Membership.objects.get(
            user=invitation.issued_by,
            circle=circle
        )
        issuer.used_invitations+=1
        issuer.remaining_invitation-=1
        issuer.save()
        return member

