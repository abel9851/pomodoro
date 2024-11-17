from django.urls import path
from .views import TaskListView

app_name = "tasks"

urlpatterns = [
    # 익명유저 전용 task list api
    path("", TaskListView.as_view(), name="task_list")
]
