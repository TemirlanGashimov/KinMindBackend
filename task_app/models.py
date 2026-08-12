from django.db import models

# Create your models here.

class Task(models.Model):
    board = models.ForeignKey('board_app.Board', on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=[('todo', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done')], default='todo')
    priority = models.CharField(max_length=50, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    assignee_id = models.IntegerField(null=True, blank=True)
    reviewer_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title