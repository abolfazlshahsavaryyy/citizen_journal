from django.urls import path
from Question.views.question_view import QuestionListCreateView, QuestionUpdateDeleteView

urlpatterns = [
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionUpdateDeleteView.as_view(), name='question-detail-update-delete'),
]
