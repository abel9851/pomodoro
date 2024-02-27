
from drf_spectacular.utils import extend_schema
from tasks.serializers import TaskDetailSerializer
from api.permissions import IsAuthenticatedAndIsObjectOwner
from rest_framework.views import APIView
from api_utils.common import get_model_instance_by_pk_or_not_found

from tasks.models import Task
from rest_framework.response import Response
from rest_framework import status


# TODO: Task put(외래키관계인 pomodoro의 증감), delete, get
# put에 관해서는 Task 자체의 정보의 수정과 Task과 연관된 pomodoro의 증감이 가능하게 할 것
# Task 정보를 수정하는데 쿼리 1개, 프론트로부터 Task의 편집화면에서 개수를 조절할 수 있는 업 앤 다운 버튼이 있고
# 늘어나면 새로운 pomodoro를 추가, 줄면 맨 마지막 추가했던 pomodoro를 삭제하도록 하자.
# pomodoro를 개별 조작 및 삭제 할 의도가 없었다면, pomodoro 모델을 만들 필요도 없이
# Task에서 pomodoro모델에 저장한 시간과, 포모도로 개수를 Task 모델에 전부 저장하고
# pomodoro count 컬럼을 추가하고, 거기에 개수를 저장해서 pomodoro를 프론트에서 생성했었으면 됬었다.
# 하지만 pomodoro를 개별 조작하는게 이번에 하고 싶은 기능이기 때문에 유지하되
# TaskDetailView
# TODO: 01/12에 api 호출 테스트하기, TaskDetail에는 project의 pk가 필요 없으므로
# view의 위치를 task app으로 옮기기
class TaskDetailView(APIView):
    permission_classes = [IsAuthenticatedAndIsObjectOwner]

    @extend_schema(
        description="Task Detail",
        responses={200: TaskDetailSerializer},)
    def get(self, request, task_pk):
        # 해당 task를 소유한 유저인지 확인
        task = get_model_instance_by_pk_or_not_found(Task, task_pk)
        serializer = TaskDetailSerializer(task)

        return Response(serializer.data, status=status.HTTP_200_OK)

        # 해당 task를 취득

        # 해당 task를 직렬화

    def put(self, request, project_pk, task_pk):
        pass

    def delete(self, request, project_pk, task_pk):
        pass

# TODO: pomodoro 하나하나 get, put, delete - 나중에 구현되는 것들.
