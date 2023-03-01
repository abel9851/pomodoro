from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserLoginTokenObtainPairSerializer


class UserApiLogin(TokenObtainPairView):

    """simple jwt를 상속해서 커스텀한 login view"""

    def post(self, request):
        serializer = UserLoginTokenObtainPairSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserApiLogout(APIView):
    def post(self, request):

        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token is not None:
            token = RefreshToken(refresh_token)
            token.blacklist()

        response = Response()
        response.delete_cookie("refresh_token")
        return response
