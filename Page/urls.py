# myapp/urls.py

from django.urls import path
from Page.views.page_views import *
from Page.views.follow_views import FollowDetailesView,FollowListView

urlpatterns = [
    path('pages/', PageListCreateView.as_view(), name='page-list-create'),
    path('pages/<int:pk>/', PageDetailView.as_view(), name='page-detail'),
    path('follow/',FollowListView.as_view(),name='follow-create'),
    path('follow/<int:pk>/', FollowDetailesView.as_view(),name='follow-details')
]
