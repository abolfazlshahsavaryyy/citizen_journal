
from Comment.models import Comment
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
import requests
import logging
logger = logging.getLogger(__name__)

PREDICT_API_URL = "http://hate_speech_api:8000/predict"  # Change if needed

def create_comment(user, content, news, reply=None):
    """
    Create a comment or reply.
    Sends comment content to hate speech prediction API and stores the probability in hate_rate.
    """
    # If reply is provided, ensure it belongs to the same news
    if reply is not None and reply.news != news:
        raise ValidationError("Reply must belong to the same news as the parent comment.")

    # --- Call the prediction API ---
    try:
        response = requests.post(PREDICT_API_URL, json={"content": content})
        logger.info(f"Response status: {response.status_code}, body: {response.text}")
        response.raise_for_status()
        data = response.json()
        hate_rate = data.get("probability", 0.5)
    except Exception as e:
        logger.error(f"Prediction API error: {e}", exc_info=True)
        hate_rate = 3.14

    # --- Create the comment ---
    comment = Comment.objects.create(
        user=user,
        content=content,
        news=news,
        reply=reply,
        hate_rate=hate_rate
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
