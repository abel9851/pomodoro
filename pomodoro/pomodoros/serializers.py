from rest_framework import serializers

from .models import Pomodoro


class PomodoroCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pomodoro
        fields = ["id", "pomodoro_length", "break_length"]
