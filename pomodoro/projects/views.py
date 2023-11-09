from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

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


# TODO: projects List View를 생성한 뒤 기능 구현 할 것.
class TaskListView(APIView):
    def post(self, request):
        # request.data를 serializer로 검증
        # 검증된 데이터로 Task 생성
        # task가 속한 project를 확인 - project의 id를 url로 받아야한다.
        #

        return Response()
