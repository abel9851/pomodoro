from django.urls import path
from users.views import UserApiLogin, UserApiLogout

app_name = "api"

urlpatterns = [
    path("users/login/", UserApiLogin.as_view(), name="login"),
    path("users/logout/", UserApiLogout.as_view(), name="logout"),
]
