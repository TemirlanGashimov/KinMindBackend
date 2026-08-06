from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from board_app.models import Board
from .serializers import BoardSerializer, BoardCreateSerializer



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