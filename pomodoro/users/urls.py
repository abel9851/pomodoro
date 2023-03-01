from django.urls import path

from .views import UserApiLogin, UserApiLogout

urlpatterns = [path("login/", UserApiLogin.as_view(), name="user-login"), path("logout/", UserApiLogout.as_view(), name="user-logout")]
