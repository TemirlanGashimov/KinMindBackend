from rest_framework.permissions import BasePermission


class IsBoardOwner(BasePermission):
    """
    Permission that checks if user is the owner of a board.

    Only board owners can delete the board.
    """

    def has_object_permission(self, request, view, obj):
        """Check if user is the board owner."""
        return obj.owner == request.user


class IsBoardMemberOrOwner(BasePermission):
    """
    Permission that checks if user is the owner or a member of a board.
    """

    def has_object_permission(self, request, view, obj):
        """Check if user has access to the board."""
        return (
            obj.owner == request.user
            or obj.members.filter(id=request.user.id).exists()
        )
