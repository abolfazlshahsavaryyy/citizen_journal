from django.db import models
from django.conf import settings
class Comment(models.Model):
    content = models.CharField(
        max_length=500,
        help_text="This is the content of the comment"
    )
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    # Self-referencing foreign key to allow nested comments (replies)
    reply = models.ForeignKey(
        'self',                          # Reference to the same model
        null=True,                       # Allow top-level comments (no parent)
        blank=True,                      # Allow form field to be optional
        on_delete=models.CASCADE,       # Delete all child comments if parent is deleted
        related_name='replies',         # Allows access like: comment.replies.all()
        help_text="Optional reference to a parent comment"
    )
    hate_rate=models.FloatField(help_text='this show how hate speech is each comment')

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time the comment was created."
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time the comment was last updated."
    )

    news=models.ForeignKey(
        'Page.News',
        null=False,
        on_delete=models.CASCADE,
        related_name='post',
        help_text='each comment has to have reference to specific post'
    )

    def __str__(self):
        return f'{self.content[:20]}  ...'
