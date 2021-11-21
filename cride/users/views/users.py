"""Users view"""

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


from cride.users.serializers.users import UserLoginSerializer, UserModelSerializer


class UserLoginApiView(APIView):
    """User Login Api View"""

    def post(self, request, *args, **kwargs):
        """Handle http post view"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        print('==User',user)
        data = {
            # 'status': 'ok',
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)
