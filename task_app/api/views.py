from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from board_app.models import Board
from .serializers import TaskCreateSerializer, TaskSerializer


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

        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = self.perform_create(serializer)
        response_serializer = TaskSerializer(task)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


