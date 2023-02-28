from rest_framework import response, status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import UserLoginTokenObtainPairSerializer


class UserApiLogin(TokenObtainPairView):

    """simple jwt를 상속해서 커스텀한 login view"""

    def post(self, request):

        serializer = UserLoginTokenObtainPairSerializer(request.data)

        if serializer.is_valid():
            return response(serializer.data, status=status.HTTP_200_OK)
        else:
            # TODO 메시지 추가
            return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
