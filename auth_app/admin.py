from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model."""
    list_display = ['fullname', 'get_email', 'get_username']
    search_fields = ['fullname', 'user__email', 'user__username']
    readonly_fields = ['user']

    def get_email(self, obj):
        """Display user email."""
        return obj.user.email
    get_email.short_description = 'Email'

    def get_username(self, obj):
        """Display username."""
        return obj.user.username
    get_username.short_description = 'Username'
