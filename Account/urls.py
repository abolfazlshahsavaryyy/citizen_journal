# accounts/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('me/', ProfileDetailView.as_view(), name='profile-detail'),
    path('register/', RegisterView.as_view(), name='register'),
]
