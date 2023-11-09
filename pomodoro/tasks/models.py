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
    due_date = models.DateField(verbose_name="task due date", default=date.today)

    # TODO: repeat 기능 추가
