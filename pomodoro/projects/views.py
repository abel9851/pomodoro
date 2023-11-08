from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProjectListSerializer


# TODO: test 필요.
class ProjectListView(APIView):
    def post(self, request):
        serializer = ProjectListSerializer(request.data)

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
