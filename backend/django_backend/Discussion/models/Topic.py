from django.db import models
from Page.models.Page import Page

class Topic(models.Model):
    discussion = models.ForeignKey(
        'Discussion',
        on_delete=models.CASCADE,
        related_name='topics'
    )
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the Topic was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time the Topic was updated"
    )
    def __str__(self):
        return self.title
