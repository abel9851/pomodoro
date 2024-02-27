from django.urls import path

from .views import ProjectListView, TaskListView

app_name = "projects"

urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
    path("<int:project_pk>/tasks/", TaskListView.as_view(), name="task_list"),
]
