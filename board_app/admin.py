from django.contrib import admin

from .models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """Admin interface for Board model."""

    list_display = ['title', 'get_owner_email', 'member_count', 'ticket_count']
    list_filter = ['member_count', 'ticket_count']
    search_fields = ['title', 'owner__email']
    filter_horizontal = ['members']
    readonly_fields = ['member_count', 'ticket_count',
                       'tasks_to_do_count', 'tasks_high_prio_count']

    def get_owner_email(self, obj):
        """Display owner email address."""
        return obj.owner.email

    get_owner_email.short_description = 'Owner'
