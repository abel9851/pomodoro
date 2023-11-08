from django.urls import path

from .views import UserApiLogin, UserApiLogout

app_name = "users"

urlpatterns = [
    path("login/", UserApiLogin.as_view(), name="login"),
    path("logout/", UserApiLogout.as_view(), name="logout"),
]
