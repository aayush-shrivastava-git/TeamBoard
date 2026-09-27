from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Project, Task, Comment, KBEntry, QueryLog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    company_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "company_name"]

    def create(self, validated_data):
        company_name = validated_data.pop("company_name")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        user.company.company_name = company_name
        user.company.save()

        return user

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "owner", "members", "created_at"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "title",
            "description",
            "status",
            "assignee",
            "created_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "task",
            "author",
            "body",
            "created_at",
        ]

class KBEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = KBEntry
        fields = [
            "id",
            "question",
            "answer",
            "category",
            "created_at",
        ]

class QueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryLog
        fields = [
            "id",
            "search_term",
            "results_count",
            "queried_at",
        ]