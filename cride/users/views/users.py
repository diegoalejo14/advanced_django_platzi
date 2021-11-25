"""Users view"""

from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action


from cride.users.serializers.users import UserLoginSerializer, UserModelSerializer, UserSignUpSerializer, AccountVerificationSerializer


class UserViewSet(viewsets.GenericViewSet):
    """User View set

    Handle Sign up, login and account verification
    """

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """SignUp"""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login User"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Verify User"""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Congratulations. Your account was verified'
        }
        return Response(data, status=status.HTTP_200_OK)


# class UserLoginApiView(APIView):
#     """User Login Api View"""

#     def post(self, request, *args, **kwargs):
#         """Handle http post view"""
#         serializer = UserLoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user, token = serializer.save()
#         data = {
#             'user': UserModelSerializer(user).data,
#             'access_token': token
#         }
#         return Response(data, status=status.HTTP_201_CREATED)


# class UserSignUpView(APIView):
#     """User Sign Up Api View"""

#     def post(self, request, *args, **kwargs):
#         """Handle http post view"""
#         serializer = UserSignUpSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         data = UserModelSerializer(user).data
#         return Response(data, status=status.HTTP_201_CREATED)


# class AccountVerificationAPIView(APIView):
#     """Account Verification API view"""

#     def post(self, request, *args, **kwargs):
#         """Handle http post view"""
#         serializer = AccountVerificationSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         data = {
#             'message': 'Congratulations. Your account was verified'
#         }
#         return Response(data, status=status.HTTP_200_OK)
