from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from .serializers import UserLoginTokenObtainPairSerializer, UserLogoutSerializer


class UserApiLogin(APIView):
    # get_authenticat_header()를 사용하지 않으면 GenericAPIView랑 같으니까 안쓴다면 GenericAPIview로 바꾸기
    # genericAPIView가 뭔지 조사하기 exception자동으로 걸러주는지 확인할것.
    # 로그인 자체는 session login이 필요하다. 왜냐하면 JWT Authentication을 하면
    # username, password와 같은 credential이 아닌, token을 날려야하기 때문.
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    # AllowAny를 해놓으면 authentication을 어떻게 해놓던간에 그 api에 request를 제한없이 날릴수 있다.
    # authentication_classes를 지정하면 그 api는 식별을 authentication_class에 있는 방식으로 식별한다.
    # 그 다음 permission_classes에 IsAutenticated를 하면 request.user의 is_authenticated 메소드가 True인지 확인한다.
    # False면 그 api는 사용할 수 없다.
    # 반면에 permission_class에 AllowAny를 해놓는다면 인증이 세션인증인지 JWT인증인지, is_authtenticated가 true인지 False인지 전혀 신경쓰지않는다.
    # 즉, 자유롭게 request를 할 수 있다.

    # 3/6에 authentication 문서 읽기

    """simple jwt를 사용해서 커스텀한 login view"""

    def post(self, request):
        serializer = UserLoginTokenObtainPairSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserApiLogout(APIView):
    """jwt를 black list에 추가해서 로그아웃"""

    # test를 위해 autentication_classes는 설정하지 않는다.
    # test가 끝나면 autnetication_classes를 rest_framework_simplejwt.authentication.JWTAuthentication"로 설정할 것.
    # authentication_classes  [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
