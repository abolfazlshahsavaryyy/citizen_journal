# myapp/urls.py

from django.urls import path
from Page.views.page_views import *
from Page.views.follow_views import *
from Page.views.news_views import *

urlpatterns = [
    path('pages/', PageListCreateView.as_view(), name='page-list-create'),
    path('pages/<int:pk>/', PageDetailView.as_view(), name='page-detail'),
    path('follow/',FollowListView.as_view(),name='follow-create'),
    path('follow/<int:pk>/', FollowDetailesView.as_view(),name='follow-details'),
    path('news/', NewsListCreateView.as_view(), name='news-list-create'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail')
]
