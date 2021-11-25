"""Users Permissions"""

#Django Rest Framework

from rest_framework.permissions import BasePermission



class IsAccountOwner(BasePermission):
  """Allow access only to objects where user is the owner"""

  def has_object_permission(self,request,view,obj):
    """Verify if user is owner"""
    return request.user==obj

class IsAuthenticated(BasePermission):
  """Allow access only if user is authenticated"""

  def has_object_permission(self,request,view,obj):
    """Verify if user is authenticated"""
    pass 