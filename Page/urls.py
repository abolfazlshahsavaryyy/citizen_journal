# myapp/urls.py

from django.urls import path
from Page.views.page_views import *
from Page.views.follow_views import *
from Page.views.news_views import *
from Page.views.like_view import *

urlpatterns = [
    path('pages/', PageListCreateView.as_view(), name='page-list-create'),
    path('pages/<int:pk>/', PageDetailView.as_view(), name='page-detail'),
    path('follow/',FollowListView.as_view(),name='follow-create'),
    path('follow/<int:pk>/', FollowDetailesView.as_view(),name='follow-details'),
    path('news/', NewsListCreateView.as_view(), name='news-list-create'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('news/like/<int:news_id>/', NewsLikeView.as_view(), name='news-like'),

    path('news/unlikes/<int:news_id>', NewsUnlikeView.as_view(), name='news_unlike'),
    path('news/get_likes/<int:news_id>', NewsLikesListView.as_view(), name='news_like_get'),
    path('news/user/<int:pk>', NewsUserView.as_view(), name='news_user')

]
