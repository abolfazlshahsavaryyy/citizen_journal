# services.py
from django.db import transaction
from Notification.tasks import *
#from Page.task import send_notification
def toggle_news_like(news, user):
    with transaction.atomic():
        if news.likes.filter(id=user.id).exists():
            news.likes.remove(user)
            action = "unliked"
            message = "Unliked successfully."
        else:
            news.likes.add(user)
            action = "liked"
            message = "Liked successfully."

            # Send async notification to the owner of the news post
            if news.page.user != user:
                send_notification.delay(
                    user_id=news.page.user.id,
                    message=f"{user.username} liked your news post.",
                    data={"news_id": news.id}
                )

        news.like_count = news.likes.count()
        news.save(update_fields=["like_count"])

    return action, message
