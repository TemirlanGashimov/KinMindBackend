"""
Board API URL patterns.

Endpoints:
    - GET /api/boards/ - List user boards
    - POST /api/boards/ - Create new board
    - GET /api/boards/<id>/ - Get board details
    - PATCH /api/boards/<id>/ - Update board
    - DELETE /api/boards/<id>/ - Delete board
    - GET /api/email-check/ - Search user by email
"""
from django.urls import path

from .views import BoardListCreateView, BoardDetailView, EmailCheckView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list-create'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('email-check/', EmailCheckView.as_view(), name='email-check')
]