from core import models as core_models
from django.db import models


class Task(core_models.TimeStampedModel):
    user = models.ForeignKey(
        "users.User",
        verbose_name="releated user",
        related_name="tasks",
        on_delete=models.CASCADE,
    )
    color = models.CharField(
        verbose_name="color code", max_length=150, default="#0067c0"
    )
