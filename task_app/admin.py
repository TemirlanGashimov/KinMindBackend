from django.contrib import admin

from .models import Task, Comment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin interface for Task model."""

    list_display = ['title', 'board', 'status',
                    'priority', 'assignee', 'due_date']
    list_filter = ['status', 'priority', 'board']
    search_fields = ['title', 'description', 'board__title']
    readonly_fields = ['created_by']

    fieldsets = (
        ('Task Information', {
            'fields': ('board', 'title', 'description', 'created_by')
        }),
        ('Assignment', {
            'fields': ('assignee', 'reviewer')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'due_date')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model."""

    list_display = ['get_author_name', 'task', 'created_at']
    list_filter = ['created_at', 'task__board']
    search_fields = ['task__title', 'author__email', 'content']
    readonly_fields = ['created_at', 'author', 'task']

    def get_author_name(self, obj):
        """Display comment author name."""
        return f'{obj.author.profile.fullname} ({obj.author.email})'
    
    get_author_name.short_description = 'Author'
