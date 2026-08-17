from django.contrib.auth.models import User
from rest_framework import serializers

from board_app.api.serializers import BoardMemberSerializer
from task_app.models import Task, Comment


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new tasks.
    
    Accepts task details including board, title, description,
    status, priority, assignee, reviewer, and due date.
    """
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        required=False
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reviewer',
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'board', 'title', 'description', 'status',
            'priority', 'assignee_id', 'reviewer_id', 'due_date'
        ]


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying task information.
    
    Returns task details with member information and comment count.
    """
    assignee = BoardMemberSerializer(read_only=True)
    reviewer = BoardMemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description',
            'status', 'priority', 'assignee', 'reviewer',
            'due_date', 'comments_count'
        ]

    def get_comments_count(self, obj):
        """Return count of comments on this task."""
        return obj.comments.count()


class TaskUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating task information.
    
    Allows updating task status, priority, assignments, and due date.
    """
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        required=False
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reviewer',
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'title', 'description', 'status', 'priority',
            'assignee_id', 'reviewer_id', 'due_date'
        ]


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for task comments.
    
    Returns comment information with author name from profile.
    """
    author = serializers.CharField(
        source='author.profile.fullname',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
