from django.urls import path

from .views import UserApiLogin

urlpatterns = [path("login/", UserApiLogin.as_view(), name="user-login")]
