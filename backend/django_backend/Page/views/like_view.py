
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Page.serializer.like_serializer import *
from Page.services.like_service import *
from drf_yasg.utils import swagger_auto_schema
class NewsToggleLikeView(APIView):
    """
    POST endpoint to toggle like/unlike on a news item.
    """
    @swagger_auto_schema(
        request_body=NewsToggleLikeSerializer,
        responses={200: NewsToggleLikeSerializer}
    )
    def post(self, request):
        serializer = NewsToggleLikeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        news = serializer.validated_data["news_id"]  # validated field replaced with object
        user = request.user

        action, message = toggle_news_like(news, user)

        return Response({
            "message": message,
            "news_id": news.id,
            "like_count": news.like_count,
            "action": action  # 'liked' or 'unliked'
        }, status=status.HTTP_200_OK)




class NewsLikesListView(APIView):
    def get(self, request, news_id):
        try:
            news = News.objects.prefetch_related('likes').get(id=news_id)
        except News.DoesNotExist:
            return Response({'error': 'News not found.'}, status=404)

        users = news.likes.all()
        serializer = SimpleUserSerializer(users, many=True)
        return Response(serializer.data, status=200)

