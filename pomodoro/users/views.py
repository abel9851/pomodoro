from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserLoginTokenObtainPairSerializer, UserLogoutSerializer


class UserApiLogin(TokenObtainPairView):
    pass
    # get_authenticat_header()를 사용하지 않으면 GenericAPIView랑 같으니까 안쓴다면 GenericAPIview로 바꾸기
    # genericAPIView가 뭔지 조사하기 exception자동으로 걸러주는지 확인할것.

    """simple jwt를 상속해서 커스텀한 login view"""

    def post(self, request):
        serializer = UserLoginTokenObtainPairSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserApiLogout(APIView):
    """jwt를 black list에 추가해서 로그아웃"""

    # drf 인증,인가 강의보고 permission class 이해하고 추가하기

    def post(self, request):

        serializer = UserLogoutSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e)

        response = Response(status=status.HTTP_200_OK)

        # cookie에서 Rresh token 삭제
        # front에서는 bearer schema에 있는 access token을 삭제할 필요가 있다.
        response.delete_cookie("refresh")

        return response
