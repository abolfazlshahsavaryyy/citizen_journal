# accounts/urls.py

from django.urls import path
from Account.views.profile_view import ProfileDetailView
from Account.views.user_view import RegisterView
urlpatterns = [
    path('me/', ProfileDetailView.as_view(), name='profile-detail'),
    path('register/', RegisterView.as_view(), name='register'),
]
