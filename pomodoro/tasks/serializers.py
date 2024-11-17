from pomodoros.models import Pomodoro
from pomodoros.serializers import PomodoroCreateSerializer
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

from .models import Task


@extend_schema_serializer(
    exclude_fields=("id", "pomodoros"),
    examples=[
        OpenApiExample(
            "full fields",
            summary="Task create full fields Example",
            description="Task create full fields Example, client can choose \
                that using all fields or not",
            value={
                "name": "task name",
                "priority": 1,
                "due_date": "2021-12-12",
                "pomodoro_count": 3,
            },
            request_only=True,
        ),
        OpenApiExample(
            "required fields",
            summary="Task create required fields Example",
            description="Task create use default value Example, client can choose \
                that using required fields or all fields",
            value={
                "name": "task name",
                "pomodoro_count": 3,
            },
            request_only=True,
        ),
    ],
)
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
        # fields = ["id", "name", "pomodoro_count", "pomodoros"]

    def create(self, validated_data):
        pomodoro_count = validated_data.pop("pomodoro_count")
        project = self.context.get("project")
        task = Task.objects.create(**validated_data, project=project)
        pomodoros = [Pomodoro(task=task) for _ in range(pomodoro_count)]
        Pomodoro.objects.bulk_create(pomodoros)

        return task


class TaskDetailSerializer(serializers.ModelSerializer):
    """Task Detail Serializer"""

    # pomodoro는 task detail을 get한 뒤.
    # 유저가 pomodoro_count부분을 누르면
    # task의 id를 사용해서 별도로 pomodoro list(pomodoro의 상세내용 포함)을 get하는 api를 사용할 것이므로
    # 여기에는 포함시키지 않는다.

    class Meta:
        model = Task
        fields = ["id", "due_date", "pomodoro_count"]


class TaskListSerializer(serializers.ModelSerializer):
    """Task List Serializer"""

    class Meta:
        model = Task
        fields = ["id", "name", "priority", "pomodoro_count", "updated"]


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Task Update Serializer"""

    class Meta:
        model = Task
        fields = ["id", "name", "priority", "due_date", "pomodoro_count"]
