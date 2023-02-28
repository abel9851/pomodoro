from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserLoginTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT의 claim을 custom하기 위한 serializer"""

    # TODO 유저 로그인이 여러번 실패했을 경우에 처리 하는 기능 추가

    # TODO 로그인이 실패했을 경우, 어떻게 리턴하지는 확인하기

    # TODO parernt class에서 user_id로 claim 하는거 확인했으니까 필요한 claim 지정은 settings로 지정하기
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # add sutom claims
        token["user_pk"] = user.pk

        return token
