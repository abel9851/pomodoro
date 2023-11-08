from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("users/", include("users.urls", namespace="users")),
    path("tasks/", include("tasks.urls", namespace="tasks")),
]
