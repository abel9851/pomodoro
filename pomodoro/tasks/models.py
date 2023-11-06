from core import models as core_models
from django.db import models


class Task(core_models.TimeStampedModel):
    """Task Model Definition"""

    name = models.CharField(verbose_name="task name", max_length=200)
    memo = models.CharField(verbose_name="task memo", max_length=300)
    # db에 저장되는 건 integer, client에 표시되는 것은 글자가 표시되도록 하기.
    # TODO: 231108 priority choice & due_date 날짜확인해서 project 분류 가능한가 확인하기
    # priority = models.IntegerField()
    # due_date = models.DateTimeField()

    # TODO: repeat 기능 추가

    # color = models.CharField(
    #     verbose_name="color code", max_length=150, default="#0067c0"
    # )
