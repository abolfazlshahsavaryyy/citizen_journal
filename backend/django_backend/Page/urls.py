# myapp/urls.py

from django.urls import path
from Page.views.page_views import *
from Page.views.follow_views import *
from Page.views.news_views import *
from Page.views.like_view import *

urlpatterns = [
    path('pages/', PageListCreateView.as_view(), name='page-list-create'),
    path('pages/<int:pk>/', PageDetailView.as_view(), name='page-detail'),
    path('pages/follow/', ToggleFollowPageView.as_view(), name='follow-page'),
    path('news/', NewsListCreateView.as_view(), name='news-list-create'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('news/like/', NewsToggleLikeView.as_view(), name='news-like'),
    
    
    path('news/get_likes/<int:news_id>', NewsLikesListView.as_view(), name='news_like_get'),
    path('news/user/<int:pk>', NewsUserView.as_view(), name='news_user'),
    path('pages/<int:page_id>/followers/', PageFollowersView.as_view(), name='page-followers'),
    path('pages/<int:page_id>/following/', PageFollowingView.as_view(), name='page-following'),
    path('predict-news/<int:news_id>/', PredictNewsView.as_view(), name='predict-news'),
    path('api/news/search/', NewsSearchView.as_view(), name='news-search'),

]
