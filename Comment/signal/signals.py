from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from Comment.models import Comment
from Page.models import News

@receiver(post_save, sender=Comment)
def increment_comment_count(sender, instance, created, **kwargs):
    if created and instance.news:
        instance.news.comment_count = instance.news.comment_count + 1
        instance.news.save(update_fields=['comment_count'])

@receiver(post_delete, sender=Comment)
def decrement_comment_count(sender, instance, **kwargs):
    if instance.news and instance.news.comment_count > 0:
        instance.news.comment_count = instance.news.comment_count - 1
        instance.news.save(update_fields=['comment_count'])
