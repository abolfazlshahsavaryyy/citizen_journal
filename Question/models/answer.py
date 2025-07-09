from django.db import models
from Question.models.question import Question

class Answer(models.Model):
    content = models.TextField(help_text="The content of the answer.")
    

    # ForeignKey to Question
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer(id={self.id}, question_id={self.question.id})"
