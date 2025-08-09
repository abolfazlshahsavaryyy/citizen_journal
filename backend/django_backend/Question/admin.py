from django.contrib import admin
from Question.models.question import Question
from Question.models.answer import Answer
# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)