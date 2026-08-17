from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    """
    Task model representing a task/ticket in a kanban board.
    
    Attributes:
        board: ForeignKey to the Board this task belongs to
        title: Task title/summary
        description: Detailed task description
        status: Current status of the task (todo, in_progress, review, done)
        priority: Task priority level (low, medium, high)
        assignee: User assigned to work on this task
        reviewer: User responsible for reviewing this task
        created_by: User who created the task
        due_date: Optional due date for task completion
    """
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    board = models.ForeignKey(
        'board_app.Board',
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='todo'
    )
    priority = models.CharField(
        max_length=50,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_tasks'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-id']

    def __str__(self):
        return f'{self.title} (Status: {self.get_status_display()})'


class Comment(models.Model):
    """
    Comment model for task discussions.
    
    Attributes:
        task: ForeignKey to the Task this comment belongs to
        author: User who wrote the comment
        content: Comment text content
        created_at: Timestamp when the comment was created
    """
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.email} on {self.task.title}'
