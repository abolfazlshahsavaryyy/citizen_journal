
from Comment.models import Comment
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

def create_comment(user, content, news, reply=None):
    """
    Create a comment or reply.
    Ensures reply (if provided) belongs to the same news.
    """
    # If reply is provided, ensure it belongs to the same news
    if reply is not None:
        if reply.news != news:
            raise ValidationError("Reply must belong to the same news as the parent comment.")

    comment = Comment.objects.create(
        user=user,
        content=content,
        news=news,
        reply=reply
    )
    return comment



def update_comment(user, comment_id, data):
    """
    Update comment content if user is the owner.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.user != user:
        raise PermissionDenied("You are not allowed to update this comment.")

    # Update fields
    for field, value in data.items():
        setattr(comment, field, value)
    comment.save()

    return comment


def delete_comment(user, comment_id):
    """
    Delete comment if user is the owner.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.user != user:
        raise PermissionDenied("You are not allowed to delete this comment.")

    comment.delete()
    return True
