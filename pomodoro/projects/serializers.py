from rest_framework import serializers

from .models import Project


class ProjectListSerializer(serializers.ModelSerializer):
    """Project List Model Serializer"""

    class Meta:
        model = Project
        fields = ["name", "description", "color", "is_active"]


class ProjectCreateRequestSerializer(serializers.ModelSerializer):
    """
    Project Request Create Model Serializer
    only use for openapi request parameter
    """

    class Meta:
        model = Project
        fields = ["name", "description", "color", "is_active"]


class ProjectCreateSerializer(serializers.ModelSerializer):
    """Project Create Model Serializer"""

    class Meta:
        model = Project
        fields = ["name", "description", "color", "is_active"]


# TODO: 10/12 TaskDetailSerializer에 nested serializer인
# rojectDetailSerializer에는 field가 id와 name만 필요하므로
# ProjectDetailSerializer라는 이름이 적절하지 않다고 생각한다.
# 이름을 변경하자.
class ProjectBasicInfoSerializer(serializers.ModelSerializer):
    """Project Detail Model Serializer"""

    class Meta:
        model = Project
        fields = ["id", "name"]
