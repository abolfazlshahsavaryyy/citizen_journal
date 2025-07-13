# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Page.models import News
from Page.serializer.news_serializer import NewsCreateSerializer, NewsReadSerializer
from django.shortcuts import get_object_or_404
from Page.models import Page
from drf_yasg.utils import swagger_auto_schema

class NewsListCreateView(APIView):
    def get(self, request):
        news_list = News.objects.all()
        serializer = NewsReadSerializer(news_list, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(
        request_body=NewsCreateSerializer,
        responses={201: NewsCreateSerializer}
    )
    def post(self, request):
        serializer = NewsCreateSerializer(data=request.data)

        if serializer.is_valid():
            page = serializer.validated_data['page']

            # ✅ Prevent posting to someone else's page
            if page.user != request.user:
                return Response(
                    {'error': 'You are not the owner of this page.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            news = serializer.save()
            read_serializer = NewsReadSerializer(news)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(News, pk=pk)

    def get(self, request, pk):
        news = self.get_object(pk)
        serializer = NewsReadSerializer(news)
        return Response(serializer.data)
    @swagger_auto_schema(
        request_body=NewsCreateSerializer,
        responses={201: NewsCreateSerializer}
    )
    def put(self, request, pk):
        news = self.get_object(pk)

        # ✅ Ownership check
        if news.page.user != request.user:
            return Response(
                {'error': 'You are not allowed to update this news post.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = NewsCreateSerializer(news, data=request.data, partial=True)
        if serializer.is_valid():
            news = serializer.save()
            read_serializer = NewsReadSerializer(news)
            return Response(read_serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            news = self.get_object(pk)  # assumes you're in a DRF ViewSet or APIView

            page = news.page  # ✅ Proper way to access the related page
            if(page.user!=request.user):
                return Response(
                    {'error':'owenership error'},
                    status=status.HTTP_403_FORBIDDEN
                )
            if page.post_count > 0:
                page.post_count -= 1
                page.save()

            news.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except News.DoesNotExist:
            return Response({"error": "News post not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class NewsUserView(APIView):
    

    def get(self, request,pk):
        # Get the current user
        user = request.user

        # Get all pages that belong to this user
        user_pages = Page.objects.filter(user=user)

        # Get all news posts for these pages (in a single query using __in)
        user_news = News.objects.filter(page__in=user_pages).select_related('page').order_by('-published_date')

        # Serialize the news posts
        serializer = NewsReadSerializer(user_news, many=True)

        return Response(serializer.data)


