# services.py
from django.db import transaction

def toggle_news_like(news, user):
    """
    Toggles the like status of a news post for a user.
    Returns:
      (action: str, message: str)
      action = 'liked' or 'unliked'
    """
    with transaction.atomic():
        if news.likes.filter(id=user.id).exists():
            # User already liked → remove
            news.likes.remove(user)
            action = "unliked"
            message = "Unliked successfully."
        else:
            # User has not liked → add
            news.likes.add(user)
            action = "liked"
            message = "Liked successfully."

        # Update like_count
        news.like_count = news.likes.count()
        news.save(update_fields=["like_count"])

    return action, message
