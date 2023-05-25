from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken


class UserLoginTokenObtainPairSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["password"] = serializers.CharField(style={"input_type": "passowrd"}, write_only=True)

    def validate(self, attrs):
        # TODO 유저 로그인이 여러번 실패했을 경우에 처리 하는 기능 추가
        # authenticate 처리 확인하기 노마드코더
        authenticate_kwargs = {self.username_field: attrs[self.username_field], "password": attrs["password"]}

        user = authenticate(**authenticate_kwargs)

        if user:
            refresh = RefreshToken.for_user(user)
            data = {}
            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, self.user)

            return data

        else:
            raise exceptions.AuthenticationFailed


class UserLogoutSerializer(serializers.Serializer):
    """refresh token을 파기하기 위한 serializer"""

    refresh_token = serializers.CharField(allow_null=False)

    def validate(self, attrs):
        refresh_token = RefreshToken(attrs["refresh_token"])
        refresh_token.blacklist()

        return attrs
