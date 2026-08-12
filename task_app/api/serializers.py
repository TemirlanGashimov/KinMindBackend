from django.contrib.auth.models import User
from rest_framework import serializers
from task_app.models import Task
from board_app.api.serializers import BoardMemberSerializer


class TaskCreateSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assignee')
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reviewer')

    class Meta:
        model = Task
        fields = ['board', 'title', 'description', 'status',
                  'priority', 'assignee_id', 'reviewer_id', 'due_date']


class TaskSerializer(serializers.ModelSerializer):
    assignee = BoardMemberSerializer(read_only=True)
    reviewer = BoardMemberSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status',
                  'priority', 'assignee', 'reviewer', 'due_date']
