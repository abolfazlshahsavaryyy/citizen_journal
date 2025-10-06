from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path("home/", home_view, name="home"),
    path('news/<int:news_id>/', news_detail_view, name='news_detail'),
    path('news/<int:news_id>/comments/', news_comments_view, name='news_comments'),
    path("comment/<int:comment_id>/", comment_detail_view, name="comment_detail"),
]
