from datetime import date

from core import models as core_models
from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(core_models.TimeStampedModel):
    """Task Model Definition"""

    class Meta:
        db_table = "tasks"

    class Priority(models.IntegerChoices):
        HIGH = 0, _("HIGH")
        MEDIUM = 1, _("MEDIUM")
        LOW = 2, _("LOW")

    name = models.CharField(verbose_name="task name", max_length=200)
    memo = models.CharField(
        verbose_name="task memo", max_length=300, default="", blank=True
    )
    # TODO: db에 저장되는 건 integer, client에 표시되는 것은 글자가 표시되도록 하기. -> frontend에서 직접 작성해야한다.
    priority = models.IntegerField(
        verbose_name="task priority", choices=Priority.choices, default=Priority.MEDIUM
    )
    project = models.ForeignKey(
        "projects.Project",
        verbose_name="related project",
        related_name="tasks",
        on_delete=models.SET_NULL,
        null=True,
    )
    due_date = models.DateField(verbose_name="task due date", default=date.today)
    # integerfield에서는 max_length가 무시된다. Min or MaxValueValidator를 사용하던가
    # serializer에서 체크하는게 좋다.
    pomodoro_count = models.IntegerField(verbose_name="task pomodoro count", default=1)

    # TODO: is_completed 추가. 프론트에서 is_completed를 누르면 True로 되고, Project는 complete로 변경.
    # TODO: is_completed가 True가 된 날짜 추가.
    # TODO: repeat 기능 추가
