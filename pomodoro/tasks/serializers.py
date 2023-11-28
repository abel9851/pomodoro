from pomodoros.models import Pomodoro
from pomodoros.serializers import PomodoroCreateSerializer
from rest_framework import serializers

from .models import Task


class TaskPomodoroCreateSerializer(serializers.ModelSerializer):
    """Task Create model Serializer"""

    pomodoro_count = serializers.IntegerField(
        max_value=42, min_value=1, write_only=True
    )
    # TODO: Pomodoro의 데이터도 같이 response할 수 있도록 필드 추가하기 231124
    # https://www.django-rest-framework.org/api-guide/relations/
    pomodoros = PomodoroCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ["name", "pomodoro_count", "pomodoros"]

    def create(self, validated_data):
        pomodoro_count = validated_data.pop("pomodoro_count")
        task = Task.objects.create(**validated_data)
        pomodoros = [Pomodoro(task=task) for _ in range(pomodoro_count)]
        Pomodoro.objects.bulk_create(pomodoros)

        return task

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
