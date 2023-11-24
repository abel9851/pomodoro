from core import models as core_models

from django.db import models


class Pomodoro(core_models.TimeStampedModel):
    """Pomodoro Model Definition"""

    class Meta:
        db_table = "pomodoros"

    pomodoro_length = models.IntegerField(
        verbose_name="pomodoro time length", default=25
    )
    break_length = models.IntegerField(verbose_name="break time length", default=5)
    # TODO: squash 해보기
    task = models.ForeignKey(
        "tasks.Task",
        verbose_name="related task",
        related_name="pomodoros",
        on_delete=models.CASCADE,
    )
