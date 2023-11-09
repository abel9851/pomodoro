from rest_framework import serializers

from .models import Project


class ProjectListSerializer(serializers.ModelSerializer):
    """Project List Model Serializer"""

    class Meta:
        model = Project
        fields = ["name", "description", "color", "is_active"]


class ProjectCreateSerializer(serializers.ModelSerializer):
    """Project Create Model Serializer"""

    class Meta:
        model = Project
        fields = ["name", "description", "color", "is_active"]
