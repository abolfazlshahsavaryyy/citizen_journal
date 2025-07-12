# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Page.models import News
from django.contrib.auth import get_user_model
from Page.serializer.like_serializer import NewsLikeCreateSerializer, NewsLikeReadSerializer

User = get_user_model()

class NewsLikeView(APIView):
    def post(self, request):
        serializer = NewsLikeCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        likes_data = []
        for news in News.objects.prefetch_related('likes'):
            for user in news.likes.all():
                likes_data.append({'news_id': news.id, 'user_id': user.id})
        serializer = NewsLikeReadSerializer(likes_data, many=True)
        return Response(serializer.data)


class NewsUnlikeView(APIView):
    def delete(self, request):
        news_id = request.data.get('news_id')
        user_id = request.data.get('user_id')
        try:
            news = News.objects.get(id=news_id)
            user = User.objects.get(id=user_id)
        except (News.DoesNotExist, User.DoesNotExist):
            return Response({'error': 'News or User not found.'}, status=404)

        news.likes.remove(user)
        news.like_count = news.likes.count()
        news.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
