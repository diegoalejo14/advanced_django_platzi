"""Users  URLS."""

from django.urls import path
#Views
from cride.users.views.users import UserLoginApiView

urlpatterns=[
  path('users/login',UserLoginApiView.as_view())
]