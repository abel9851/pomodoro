from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from tasks.serializers import TaskPomodoroCreateSerializer

from django.db import transaction

from .models import Project
from .serializers import ProjectCreateSerializer, ProjectListSerializer

# TODO: test 필요.
# projects 모델 취득 - filter request.user의 id
# permission과 authentication은 default를 사용
# ProjectListSerializer를 사용해서 직렬화
# Response로 반환
# 사용해야 할 것은, only 메소드


class ProjectListView(APIView):
    """Project List View"""

    def get(self, request):
        projects = Project.objects.filter(user=request.user).only(
            "name", "description", "color", "is_active"
        )
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# TODO: projects List View를 생성한 뒤 기능 구현 할 것. 231121부터 할 것.
# solid 원칙의 SRP 습득으로 인해 TaskPomodoroCreateserializer만 생성함. 231121
# TODO: 231122에 마저 구현. pomodoro에 대해서는 client에서 받은 pomodoro_count를 사용해서 bulk_create가 되는지
# 확인한후, 그리고 save가 아니니까 add_auto_now가 제대로 작동안할수 있으니 이부분 조사하고 해결해서 구현하기
# pomodoro를 생성할 때에는 time length는 default값을 지정해서 처리하기
# TODO: 나중에 pomodoro의 default값을 저장하는 table을 따로 만들어서 참조해서 생성하도록 수정하기
class TaskListView(APIView):
    def post(self, request, pk):
        # request.data를 serializer로 검증
        # 검증된 데이터로 Task 생성
        # task가 속한 project를 확인 - project의 id를 url로 받아야한다.
        # post로 받는 json은 pomodoro의 개수와 task의 이름

        serializer = TaskPomodoroCreateSerializer(data=request.data)

        # raise_exception은
        # validate를 통과하지 못할 시, 400 bad request를 응답한다.
        # validate를 통과하지 못할 시의 커스텀 response를 정의하지 않는다면
        # 옵션 설정 하나로 변하게 코드를 작성할 수 있다.
        serializer.is_valid(raise_exception=True)
        # data는 name과 pomodoro_count다. pomodoro_count는 Task에 필요없는 데이터인데
        # 이 경우에는 어떻게 처리될까?
        # TypeError unexpected keyword arguments 'pomodoro_count'가 나온다.
        # 그러므로 pop을 해줘서 pomodoro_count는 별도로 취득한다.
        with transaction.atomic():
            # TODO: projects에 정의되어잇는 ManyToMany를 여기에 정의해서 처리하도록 한다.
            try:
                project = Project.objects.get(id=pk)
            except Project.DoesNotExist:
                raise NotFound(detail="Project Not Found")
            task = serializer.save()
            project.tasks.add(task)

        # TODO: 생성된 Task과 Pomodoro의 데이터를 response에 받을 수 있도록
        return Response(serializer.data, status=status.HTTP_201_CREATED)
