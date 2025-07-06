# myapp/urls.py

from django.urls import path
from .views import PageListCreateView

urlpatterns = [
    path('pages/', PageListCreateView.as_view(), name='page-list-create'),
    #path('pages/<int:pk>/', PageDetailView.as_view(), name='page-detail'),
]
