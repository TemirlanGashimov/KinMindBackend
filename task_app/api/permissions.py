from rest_framework.permissions import BasePermission


class IsCommentAuthor(BasePermission):
    """
    Permission that checks if user is the author of a comment.
    
    Only comment authors can delete their comments.
    """

    def has_object_permission(self, request, view, obj):
        """Check if user is the comment author."""
        return obj.author == request.user


class IsTaskCreatorOrBoardOwner(BasePermission):
    """
    Permission that checks if user created the task or owns the board.
    
    Only task creator or board owner can delete the task.
    """

    def has_object_permission(self, request, view, obj):
        """Check if user is task creator or board owner."""
        return (
            obj.created_by == request.user
            or obj.board.owner == request.user
        )


class IsBoardMemberOrOwner(BasePermission):
    """
    Permission that checks if user is a board member or owner.
    
    Board members and owners can access board resources.
    """

    def has_object_permission(self, request, view, obj):
        """Check if user is board member or owner."""
        return (
            obj.board.owner == request.user
            or obj.board.members.filter(id=request.user.id).exists()
        )