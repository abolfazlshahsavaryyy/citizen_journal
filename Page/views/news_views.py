# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Page.models import News
from Page.serializer.news_serializer import NewsCreateSerializer, NewsReadSerializer
from django.shortcuts import get_object_or_404


class NewsListCreateView(APIView):
    def get(self, request):
        news_list = News.objects.all()
        serializer = NewsReadSerializer(news_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NewsCreateSerializer(data=request.data)
        if serializer.is_valid():
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

    def put(self, request, pk):
        news = self.get_object(pk)
        serializer = NewsCreateSerializer(news, data=request.data, partial=True)
        if serializer.is_valid():
            news = serializer.save()
            read_serializer = NewsReadSerializer(news)
            return Response(read_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        news = self.get_object(pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
