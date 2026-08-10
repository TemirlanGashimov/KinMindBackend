from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from board_app.models import Board
from .serializers import BoardSerializer, BoardCreateSerializer, BoardUpdateSerializer, BoardDetailSerializer, BoardMemberSerializer


class BoardListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(
            Q(owner=self.request.user) |
            Q(members=self.request.user)
        ).distinct()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BoardCreateSerializer
        return BoardSerializer

    def perform_create(self, serializer):
        board = serializer.save(owner=self.request.user)
        board.members.add(self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(
            Q(owner=self.request.user) |
            Q(members=self.request.user)
        ).distinct()

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return BoardUpdateSerializer
        return BoardDetailSerializer

    def destroy(self, request, *args, **kwargs):
        board = self.get_object()

        if board.owner != request.user:
            return Response(
                {'detail': 'You do not have permission to delete this board.'},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().destroy(request, *args, **kwargs)


class EmailCheckView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email')

        if not email:
            return Response(
                {'detail': 'Email parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {'detail': 'Email not found.'},
                status=status.HTTP_404_NOT_FOUND)

        serializer = BoardMemberSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
