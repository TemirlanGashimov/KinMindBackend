from django.db.models import Q
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from board_app.models import Board
from task_app.models import Comment, Task
from .permissions import (
    IsCommentAuthor, IsTaskCreatorOrBoardOwner, IsBoardMemberOrOwner
)
from .serializers import (
    TaskCreateSerializer, TaskSerializer, TaskUpdateSerializer, CommentSerializer
)


class TaskCreateView(generics.CreateAPIView):
    """
    API endpoint for creating tasks.
    
    POST:
        - Creates a new task in a board
        - Validates user has access to the board
        - Status: 201 CREATED
        - Requires: IsAuthenticated
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TaskCreateSerializer

    def perform_create(self, serializer):
        """Validate board access and create task."""
        board = serializer.validated_data['board']
        self._validate_board_access(board)
        return serializer.save(created_by=self.request.user)

    def _validate_board_access(self, board):
        """Check if user has access to board."""
        has_access = Board.objects.filter(
            Q(id=board.id),
            Q(owner=self.request.user) |
            Q(members=self.request.user)
        ).exists()

        if not has_access:
            raise PermissionDenied(
                'You do not have permission to create a task in this board.'
            )

    def create(self, request, *args, **kwargs):
        """Handle task creation request."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = self.perform_create(serializer)
        response_serializer = TaskSerializer(task)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting tasks.
    
    GET:
        - Returns task details
        - Status: 200 OK
        - Requires: IsAuthenticated
    
    PATCH:
        - Updates task information
        - Status: 200 OK
        - Requires: IsAuthenticated
    
    DELETE:
        - Deletes task (only by creator or board owner)
        - Status: 204 NO CONTENT
        - Requires: IsTaskCreatorOrBoardOwner
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TaskUpdateSerializer

    def get_permissions(self):
        """Require ownership only for delete operations."""
        if self.request.method == 'DELETE':
            return [
                IsAuthenticated(),
                IsTaskCreatorOrBoardOwner()
            ]

        return [IsAuthenticated()]

    def get_queryset(self):
        """Return tasks accessible to current user."""
        return Task.objects.filter(
            Q(board__owner=self.request.user) |
            Q(board__members=self.request.user)
        ).distinct()

    def partial_update(self, request, *args, **kwargs):
        """Handle task update request."""
        task = self.get_object()

        serializer = self.get_serializer(
            task,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        task = serializer.save()

        response_serializer = TaskSerializer(task)
        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )


class AssignedToMeView(generics.ListAPIView):
    """
    API endpoint for listing tasks assigned to current user.
    
    GET:
        - Returns list of tasks assigned to the current user
        - Status: 200 OK
        - Requires: IsAuthenticated
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        """Return tasks assigned to current user."""
        return Task.objects.filter(
            assignee=self.request.user
        )


class ReviewingView(generics.ListAPIView):
    """
    API endpoint for listing tasks under review by current user.
    
    GET:
        - Returns list of tasks where user is reviewer
        - Status: 200 OK
        - Requires: IsAuthenticated
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        """Return tasks where user is reviewer."""
        return Task.objects.filter(
            reviewer=self.request.user
        )


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating task comments.
    
    GET:
        - Returns list of comments for a task
        - Status: 200 OK
        - Requires: IsAuthenticated, IsBoardMemberOrOwner
    
    POST:
        - Creates a new comment on a task
        - Status: 201 CREATED
        - Requires: IsAuthenticated, IsBoardMemberOrOwner
    """
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]
    serializer_class = CommentSerializer

    def get_task(self):
        """Retrieve and validate task access."""
        task_id = self.kwargs['task_id']
        task = Task.objects.filter(id=task_id).first()

        if not task:
            raise NotFound('Task not found.')

        self.check_object_permissions(self.request, task)
        return task

    def get_queryset(self):
        """Return comments for the specified task."""
        return Comment.objects.filter(
            task=self.get_task()
        )

    def perform_create(self, serializer):
        """Create comment with current user as author."""
        serializer.save(
            task=self.get_task(),
            author=self.request.user
        )


class CommentDeleteView(generics.DestroyAPIView):
    """
    API endpoint for deleting comments.
    
    DELETE:
        - Deletes a comment (only by author)
        - Status: 204 NO CONTENT
        - Requires: IsAuthenticated, IsCommentAuthor
    """
    permission_classes = [IsAuthenticated, IsCommentAuthor]
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        """Return comments for the specified task."""
        task_id = self.kwargs['task_id']

        return Comment.objects.filter(
            task_id=task_id
        )
