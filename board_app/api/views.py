from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from board_app.models import Board
from .permissions import IsBoardOwner
from .serializers import (
    BoardSerializer, BoardCreateSerializer,
    BoardUpdateSerializer, BoardDetailSerializer,
    BoardMemberSerializer
)


class BoardListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating boards.
    
    GET:
        - Returns boards where user is owner or member
        - Status: 200 OK
        - Requires: IsAuthenticated
    
    POST:
        - Creates a new board with current user as owner
        - Status: 201 CREATED
        - Requires: IsAuthenticated
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return boards accessible to current user."""
        return Board.objects.filter(
            Q(owner=self.request.user) |
            Q(members=self.request.user)
        ).distinct()

    def get_serializer_class(self):
        """Use different serializer for POST requests."""
        if self.request.method == 'POST':
            return BoardCreateSerializer
        return BoardSerializer

    def perform_create(self, serializer):
        """Create board and add current user as owner and member."""
        board = serializer.save(owner=self.request.user)
        board.members.add(self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting boards.
    
    GET:
        - Returns detailed board information with members and tasks
        - Status: 200 OK
        - Requires: IsAuthenticated
    
    PATCH:
        - Updates board title and members
        - Status: 200 OK
        - Requires: IsAuthenticated
    
    DELETE:
        - Deletes board (only by owner)
        - Status: 204 NO CONTENT
        - Requires: IsBoardOwner
    """
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """Require ownership only for delete operations."""
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsBoardOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Return boards accessible to current user."""
        return Board.objects.filter(
            Q(owner=self.request.user) |
            Q(members=self.request.user)
        ).distinct()

    def get_serializer_class(self):
        """Use different serializer for PATCH requests."""
        if self.request.method == 'PATCH':
            return BoardUpdateSerializer
        return BoardDetailSerializer


class EmailCheckView(generics.GenericAPIView):
    """
    API endpoint for searching users by email.
    
    GET:
        - Searches user by email parameter
        - Query params: email (required)
        - Returns: User information with profile
        - Status: 200 OK / 404 NOT FOUND / 400 BAD REQUEST
        - Requires: IsAuthenticated
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Search for user by email."""
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
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BoardMemberSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
