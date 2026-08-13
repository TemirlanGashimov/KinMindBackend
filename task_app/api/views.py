from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from board_app.models import Board
from task_app.models import Task
from .serializers import TaskCreateSerializer, TaskSerializer, TaskUpdateSerializer


class TaskCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskCreateSerializer

    def perform_create(self, serializer):
        board = serializer.validated_data['board']
        has_access = Board.objects.filter(
            Q(id=board.id) & (Q(owner=self.request.user) | Q(members=self.request.user))).exists()
        if not has_access:
            raise PermissionDenied(
                "You do not have permission to create a task in this board.")

        return serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = self.perform_create(serializer)
        response_serializer = TaskSerializer(task)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskUpdateSerializer

    def get_queryset(self):
        return Task.objects.filter(
            Q(board__owner=self.request.user) |
            Q(board__members=self.request.user)
        ).distinct()

    def partial_update(self, request, *args, **kwargs):
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

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()

        if task.created_by != request.user and task.board.owner != request.user:
            raise PermissionDenied(
                "Only the task creator or board owner can delete this task."
            )

        return super().destroy(request, *args, **kwargs)


class AssignedToMeView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(
            assignee=self.request.user
        )
