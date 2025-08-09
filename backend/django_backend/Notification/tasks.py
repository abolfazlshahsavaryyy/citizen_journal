from celery import shared_task
from django.contrib.auth import get_user_model
from Notification.models import Notification  # adjust path
User = get_user_model()

@shared_task
def send_notification(user_id, message, data=None):

    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)

        Notification.objects.create(
            user=user,
            message=message,
            data=data or {}
        )
        print(f"[CELERY] ✅ Notification created for user {user_id}")

    except Exception as e:
        print(f"[CELERY] ❌ Failed to create notification: {e}")
