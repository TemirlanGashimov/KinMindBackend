from django .urls import path
from .views import TaskCreateView, TaskDetailView, AssignedToMeView

urlpatterns = [
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(),name='task-detail'),
    path('tasks/assigned-to-me/', AssignedToMeView.as_view(), name='assigned-list'),
]

