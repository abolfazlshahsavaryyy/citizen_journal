from django.urls import path
from Discussion.Views.discussion_view import *
from Discussion.Views.topic_view import *
urlpatterns = [
    path('discussions/', DiscussionListCreateView.as_view(), name='discussion-list-create'),
    path('discussions/<int:pk>/', DiscussionDetailView.as_view(), name='discussion-detail'),
    path('topics/', TopicListCreateView.as_view(), name='topic-list-create'),
    path('topics/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),
    path('discussions/create/<int:page_pk>', DiscussionCreateForPageView.as_view(), name='discussion-create-for-page'),
    path('discussions/<int:discussion_id>/topics/', GetTopicOfDiscussion.as_view(), name='discussion-topics'),

]
