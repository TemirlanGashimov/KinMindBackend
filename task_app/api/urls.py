"""
Task API URL patterns.

Endpoints:
    - POST /api/tasks/ - Create new task
    - GET /api/tasks/<id>/ - Get task details
    - PATCH /api/tasks/<id>/ - Update task
    - DELETE /api/tasks/<id>/ - Delete task
    - GET /api/tasks/assigned-to-me/ - List tasks assigned to user
    - GET /api/tasks/reviewing/ - List tasks user is reviewing
    - GET /api/tasks/<id>/comments/ - List task comments
    - POST /api/tasks/<id>/comments/ - Create comment on task
    - DELETE /api/tasks/<id>/comments/<comment_id>/ - Delete comment
"""
from django.urls import path

from .views import (
    TaskCreateView, TaskDetailView, AssignedToMeView, ReviewingView,
    CommentListCreateAPIView, CommentDeleteView
)

urlpatterns = [
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/assigned-to-me/', AssignedToMeView.as_view(), name='assigned-list'),
    path('tasks/reviewing/', ReviewingView.as_view(), name='reviewing-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:task_id>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('tasks/<int:task_id>/comments/<int:comment_id>/', CommentDeleteView.as_view(), name='comment-delete'),
]

