from django.db import models
from django.conf import settings
from Discussion.models import Topic

class Question(models.Model):
    content = models.TextField(help_text="The text/content of the question.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    # Your two custom columns (as examples):
    
    is_private = models.BooleanField(default=True)

    # ForeignKey to Topic
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return f"Question(id={self.id}, topic={self.topic.title})"


