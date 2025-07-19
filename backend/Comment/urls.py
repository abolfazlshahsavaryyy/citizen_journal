from django.urls import path
from Comment.Views.comment_views import *

urlpatterns = [
    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
    path('news-comments/<int:news_pk>/', CommentNewsView.as_view(), name='news-comment'),
]
