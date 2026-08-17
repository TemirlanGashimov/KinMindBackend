from rest_framework.permissions import BasePermission


class IsBoardOwner(BasePermission):
    """
    Permission that checks if user is the owner of a board.
    
    Only board owners can delete the board.
    """

    def has_object_permission(self, request, view, obj):
        """Check if user is the board owner."""
        return obj.owner == request.user