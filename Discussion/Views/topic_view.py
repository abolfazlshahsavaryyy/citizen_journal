from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from Discussion.models import Topic
from Discussion.Serializers.topic_serializer import (
    TopicListSerializer,
    TopicDetailSerializer,
    TopicCreateSerializer,
    TopicUpdateSerializer
)


class TopicListCreateView(APIView):
    """
    Handles:
    - GET: List all topics
    - POST: Create a new topic
    """

    def get(self, request):
        topics = Topic.objects.all()
        serializer = TopicListSerializer(topics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TopicCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopicDetailView(APIView):
    """
    Handles:
    - GET: Retrieve a single topic
    - PUT: Update a topic
    - DELETE: Delete a topic
    """

    def get_object(self, pk):
        return get_object_or_404(Topic, pk=pk)

    def get(self, request, pk):
        topic = self.get_object(pk)
        serializer = TopicDetailSerializer(topic)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        topic = self.get_object(pk)
        serializer = TopicUpdateSerializer(topic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        topic = self.get_object(pk)
        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
