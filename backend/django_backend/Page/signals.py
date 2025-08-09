# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from Page.models.Page import Page
from Discussion.models.Discussion import Discussion

@receiver(post_save, sender=Page)
def create_discussion_for_page(sender, instance, created, **kwargs):
    if created:
        Discussion.objects.create(
            page=instance,
            name=f"Discussion for {instance.name}",
            description=f"Auto-created discussion for page {instance.name}"
        )
