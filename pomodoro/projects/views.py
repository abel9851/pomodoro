from api.permissions import IsAuthenticatedAndIsObjectOwner
from api_utils.model_helpers import get_model_instance_by_pk_or_not_found
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from tasks.serializers import TaskPomodoroCreateSerializer, TaskListSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import Project
from tasks.models import Task
from .serializers import ProjectListSerializer, ProjectDetailSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


# TODO: test 필요.
# projects 모델 취득 - filter request.user의 id
# permission과 authentication은 default를 사용
# ProjectListSerializer를 사용해서 직렬화
# Response로 반환
# 사용해야 할 것은, only 메소드
class ProjectListView(APIView):
    """Project List View"""

    @extend_schema(
        description="Project List",
        responses={200: ProjectListSerializer},
    )
    def get(self, request):
        # projects = Project.objects.filter(user=request.user.id).only(
        #     "name", "description", "color", "is_active"
        # )
        projects = Project.objects.only("name", "description", "color", "is_active")
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Project Create",
        request=ProjectListSerializer,
        responses={200: ProjectListSerializer},
        methods=["POST"],
    )
    def post(self, request):
        serializer = ProjectListSerializer(data=request.data)

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
# TODO: 12/12 custom permission class는 관둔다. object레벨에서 permission 체크가 행해질 경우
# response가 호출될 때 obj가 view 안에서 제어하기가 힘들다.
# common_api_util과 같은 함수로 처리하도록 하자.
# get_model_instance_by_pk_or_not_found와 느슨하게 결합해서 처리하는 방향으로 하자.
# github에서 permission_classes로 검색해서 모델 권한 제어를 어떻게 하는지 보는 것도 좋겠다.
# 수상한건 코드를 수정하기 전에는 커스텀 퍼미션 클래스가 제대로 움직였다는 것이다.
# merge이전, 12/11이전 코드로 테스트 해보자.
# 테스트 완료. DRF가 제공하는 browsable api문제였다.


# TODO: 240306에 Project detail view 만들기
class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "project_pk"
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer


class TaskListView(APIView):
    permission_classes = [IsAuthenticatedAndIsObjectOwner]

    # 호출했을 때 가져올 데이터 형식은
    # Task의 이름, pomodoro의 개수(Task에 정의되어 있음), updated된 날짜.
    # Pomodoro의 length(분). 왜냐하면 포모도로 화면에서 Task에 붙어있는 시작 버튼을 누르면
    # Pomodoro의 length를 가져와서 타이머를 돌리기 때문이다.
    # 기존의 serializer를 활용하기. 활용하게 된다면 serializer의 이름에서 create를 삭제하기
    @extend_schema(
        description="Task List",
        responses={200: TaskListSerializer},
    )
    def get(self, request, project_pk):
        tasks = Task.objects.filter(project=project_pk)
        serializer = TaskListSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Task Create",
        parameters=[
            OpenApiParameter(
                name="project_pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="project ID for which tasks are retireived",
                required=True,
                examples=[
                    OpenApiExample(
                        "Project ID",
                        summary="Project ID Example",
                        description="Project ID Example",
                        value=1,
                    ),
                ],
            ),
        ],
        request=TaskPomodoroCreateSerializer,
        responses={200: TaskPomodoroCreateSerializer},
    )
    def post(self, request, project_pk):
        # request.data를 serializer로 검증
        # 검증된 데이터로 Task 생성
        # task가 속한 project를 확인 - project의 id를 url로 받아야한다.
        # post로 받는 json은 pomodoro의 개수와 task의 이름

        # 유저 검증. 해당 Project 모델을 소유한 유저인지 확인해야한다고 생각한다.
        # TODO: 이 부분을 permission class로 해결 가능할 듯 싶다.
        # 231209 해결완료
        project = get_model_instance_by_pk_or_not_found(pk=project_pk, model=Project)
        # 240110 복습. generic view에서는 자동으로 호출되지만, APIView에서는 직접 호출해야한다.
        # generic view는 나중에 사용해보자.
        self.check_object_permissions(request, project)

        # TODO: projects와 tasks는 foreign key로 변경하기
        serializer = TaskPomodoroCreateSerializer(
            data=request.data, context={"project": project}
        )

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
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # TODO: 231209부터 아래의 작업하기
    # Project모델 인스턴스을 가리키는 Task모델 인스턴스들을 get한다.
    # get을 할 때에는 무조건 pomodoro_count를 serializer에서 반환할까 생각했는데
    # get을 할때에는 pomodoro의 이름과 pomodoro_count만 가져오기 때문에 가볍게 하기 위해
    # Task모델에 자체적으로 pomodoro_count를 갖을 것
    # query string으로 데이터를 받는다.
    # query string의 데이터로 내부에서 get하 데이터를 조회하고 파이썬 객체로 가져온다.
    # response한다.

    # request.query_params
    # serializer로 유효성 검사 및 데이터 조회
    # response 200 및 데이터 return
    # def get(self, request, pk):
    #     pass
