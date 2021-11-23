"""Users  URLS."""

from django.urls import path
# Views
from cride.users.views.users import UserLoginApiView, UserSignUpView,AccountVerificationAPIView

urlpatterns = [
    path('users/login', UserLoginApiView.as_view()),
    path('users/signup', UserSignUpView.as_view()),
    path('users/verify', AccountVerificationAPIView.as_view())
]
