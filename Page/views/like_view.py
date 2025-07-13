# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Page.models import News
from django.contrib.auth import get_user_model
from Page.serializer.like_serializer import *

User = get_user_model()

class NewsLikeView(APIView):
    def post(self, request, news_id):
        user = request.user

        try:
            news = News.objects.get(id=news_id)
        except News.DoesNotExist:
            return Response({'error': 'News not found'}, status=404)

        if news.likes.filter(id=user.id).exists():
            return Response({'message': 'Already liked'}, status=400)

        news.likes.add(user)
        news.like_count = news.likes.count()
        news.save()

        return Response({'message': 'Liked successfully', 'news_id': news.id}, status=200)

    

class NewsUnlikeView(APIView):
    def delete(self, request, news_id):
        user = request.user  # Get the current authenticated user

        try:
            news = News.objects.get(id=news_id)
        except News.DoesNotExist:
            return Response({'error': 'News not found.'}, status=404)

        if not news.likes.filter(id=user.id).exists():
            return Response({'message': 'You have not liked this news.'}, status=400)

        news.likes.remove(user)
        news.like_count = news.likes.count()
        news.save()

        return Response({'message': 'Unliked successfully.'}, status=status.HTTP_204_NO_CONTENT)


class NewsLikesListView(APIView):
    def get(self, request, news_id):
        try:
            news = News.objects.prefetch_related('likes').get(id=news_id)
        except News.DoesNotExist:
            return Response({'error': 'News not found.'}, status=404)

        users = news.likes.all()
        serializer = SimpleUserSerializer(users, many=True)
        return Response(serializer.data, status=200)

