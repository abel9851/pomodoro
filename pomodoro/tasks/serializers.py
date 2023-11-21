from rest_framework import serializers

from .models import Task


class TaskPomodoroCreateSerializer(serializers.ModelSerializer):
    """Task Create model Serializer"""

    pomodoro_count = serializers.IntegerField(max_value=42, min_value=1)

    class Meta:
        model = Task
        fields = ["name", "pomodoro_count"]
