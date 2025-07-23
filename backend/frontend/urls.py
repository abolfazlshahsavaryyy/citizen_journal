from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('page/<int:page_id>/', views.page_detail_view, name='page_detail'), 
    path('pages/news/<int:news_id>/', views.news_detail_view, name='news_detail'),
    path('pages/news/<int:news_id>/predict/', views.predict_news_view, name='predict_news'),
]
