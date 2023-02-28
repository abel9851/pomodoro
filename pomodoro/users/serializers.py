from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserLoginTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT의 claim을 custom하기 위한 serializer"""

    def validate(self, attrs):
        # TODO 유저 로그인이 여러번 실패했을 경우에 처리 하는 기능 추가
        return super().validate(attrs)
