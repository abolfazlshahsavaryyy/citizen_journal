from django.urls import path
from Discussion.Views.discussion_view import DiscussionListCreateView, DiscussionDetailView
from Discussion.Views.topic_view import TopicListCreateView, TopicDetailView
urlpatterns = [
    path('discussions/', DiscussionListCreateView.as_view(), name='discussion-list-create'),
    path('discussions/<int:pk>/', DiscussionDetailView.as_view(), name='discussion-detail'),
    path('topics/', TopicListCreateView.as_view(), name='topic-list-create'),
    path('topics/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),
]
