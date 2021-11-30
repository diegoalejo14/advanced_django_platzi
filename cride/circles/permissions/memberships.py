"""Circles permission classes."""

# Django Rest Framework

from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership


class IsActiveCircleMember(BasePermission):
    """Allow access only to circle members.


    Expect that the views implementing this permissions
    have a 'circle attribute assigned
    """
    def has_object_permission(self, request, view, obj):
        """Verify user is active member to the circle"""
        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True


class IsSelfMember(BasePermission):
    """Allow access to information if is owner"""

    def has_object_permission(self, request, view, obj):
        """Verify user is active member to the circle"""
        obj1 = view.get_object()
        return request.user == obj1.user
