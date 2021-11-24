"""Users URLs."""

# Django
from django.urls import path

# Views
from cride.users.views import AccountVerificationAPIView,    UserLoginApiView,    UserSignUpView


urlpatterns = [
    path('users/login/', UserLoginApiView.as_view(), name='login'),
    path('users/signup/', UserSignUpView.as_view(), name='signup'),
    path('users/verify/', AccountVerificationAPIView.as_view(), name='verify'),
]
