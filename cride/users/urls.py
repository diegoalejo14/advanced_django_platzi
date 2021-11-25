"""Users URLs."""

# Django
from django.urls import path , include


#Django Rest
from rest_framework.routers import DefaultRouter

# Views
#from cride.users.views import AccountVerificationAPIView,    UserLoginApiView,    UserSignUpView
from .views import users as user_views


router=DefaultRouter()
router.register(r'users',user_views.UserViewSet,basename='users')

urlpatterns = [
    path('',include(router.urls)),
    # path('users/login/', UserLoginApiView.as_view(), name='login'),
    # path('users/signup/', UserSignUpView.as_view(), name='signup'),
    # path('users/verify/', AccountVerificationAPIView.as_view(), name='verify'),

]
