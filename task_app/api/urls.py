from django .urls import path
from .views import TaskCreateView, TaskDetailView, AssignedToMeView, ReviewingView, CommentListCreateAPIView, CommentDeleteView

urlpatterns = [
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(),name='task-detail'),
    path('tasks/assigned-to-me/', AssignedToMeView.as_view(), name='assigned-list'),
    path('tasks/reviewing/', ReviewingView.as_view(),name='reviewing-list'),
    path('tasks/<int:task_id>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('tasks/<int:task_id>/comments/<int:comment_id>/',CommentDeleteView.as_view(),name='comment-delete'
)
]

