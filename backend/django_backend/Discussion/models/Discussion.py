from django.db import models
from Page.models.Page import Page
class Discussion(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Name of the discussion (e.g., group or chat title)"
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description or context for the discussion"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Can be used to archive or deactivate a discussion"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the discussion was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time the discussion was updated"
    )
    page=models.OneToOneField(Page,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
