from pomodoros.models import Pomodoro
from pomodoros.serializers import PomodoroCreateSerializer
from rest_framework import serializers

from .models import Task


class TaskPomodoroCreateSerializer(serializers.ModelSerializer):
    """Task Create model Serializer"""

    pomodoro_count = serializers.IntegerField(max_value=42, min_value=1)
    # TODO: Pomodoro의 데이터도 같이 response할 수 있도록 필드 추가하기 231124
    # read_only와 write_only로 해결.
    # Task가 pmodoro를 역참조
    pomodoros = PomodoroCreateSerializer(many=True, read_only=True)

    # read_only와 write_only를 해도 반드시 fields에 정의해야 에러가 나지 않는다.
    # Task모델을 return하고 나서 to_representation 메소드에서 write_only, read_only를 확인해서
    # 클라이언트에게 데이터로 return할 field를 결정하기 때문에
    # class Meta에 지정하는 field는 옵션관계 없이 모두 포함시켜야 한다.
    class Meta:
        model = Task
        fields = ["id", "name", "priority", "due_date", "pomodoro_count", "pomodoros"]

    def create(self, validated_data):
        pomodoro_count = validated_data.get("pomodoro_count")
        # pomodoro_count = validated_data.pop("pomodoro_count")
        task = Task.objects.create(**validated_data)
        pomodoros = [Pomodoro(task=task) for _ in range(pomodoro_count)]
        Pomodoro.objects.bulk_create(pomodoros)

        return task


# class TaskListSerializer(serializers.ModelSerializer):
#     # get해야하는 데이터: Task 이름, project이름, pomodoro 갯수
#     class Meta:
#         model = Task
#         field = ["name", ]
