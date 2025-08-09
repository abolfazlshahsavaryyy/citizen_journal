from django.urls import path
from Question.views.question_view import QuestionListCreateView, QuestionUpdateDeleteView
from Question.views.answer_view import AnswerDetailView,AnswerListCreateView
urlpatterns = [
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionUpdateDeleteView.as_view(), name='question-detail-update-delete'),
    path('answers/', AnswerListCreateView.as_view(), name='answer-list-create'),
    path('answers/<int:pk>/', AnswerDetailView.as_view(), name='answer-detail'),
]
