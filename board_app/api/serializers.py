from django.contrib.auth.models import User
from rest_framework import serializers

from board_app.models import Board
from task_app.models import Task


class BoardMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying board member information.
    
    Displays user id, email, and full name from profile.
    """
    fullname = serializers.CharField(source='profile.fullname')

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class BoardTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying tasks within a board.
    
    Includes task details with member information and comment count.
    """
    assignee = BoardMemberSerializer(read_only=True)
    reviewer = BoardMemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'assignee', 'reviewer', 'due_date', 'comments_count'
        ]

    def get_comments_count(self, obj):
        """Return count of comments on this task."""
        return obj.comments.count()


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer for listing boards.
    
    Provides summary information about boards.
    """

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'member_count', 'ticket_count',
            'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id'
        ]


class BoardCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new boards.
    
    Accepts title and members for board creation.
    """

    class Meta:
        model = Board
        fields = ['title', 'members']


class BoardUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating board information.
    
    Allows updating title and members.
    """

    class Meta:
        model = Board
        fields = ['title', 'members']


class BoardDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving detailed board information.
    
    Includes members and tasks associated with the board.
    """
    members = BoardMemberSerializer(many=True, read_only=True)
    tasks = BoardTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']
