from django.db import models
from models.question import Question
class Answer(models.Model):
    content = models.TextField(help_text="The content of the answer.")
    

    # ForeignKey to Question
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return f"Answer(id={self.id}, question_id={self.question.id})"
