from django.urls import path
from Comment.Views.comment_views import CommentListCreateAPIView, CommentDetailAPIView

urlpatterns = [
    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
]
