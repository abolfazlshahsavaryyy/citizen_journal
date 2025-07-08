from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from Discussion.models import Discussion
from Discussion.Serializers.discussion_serializer import (
    DiscussionListSerializer,
    DiscussionDetailSerializer,
    DiscussionCreateUpdateSerializer
)


class DiscussionListCreateView(APIView):
    """
    Handles GET (list all discussions) and POST (create new discussion)
    """

    def get(self, request):
        discussions = Discussion.objects.all()
        serializer = DiscussionListSerializer(discussions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DiscussionCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiscussionDetailView(APIView):
    """
    Handles GET (retrieve), PUT (update), DELETE (delete) a single discussion
    """

    def get_object(self, pk):
        return get_object_or_404(Discussion, pk=pk)

    def get(self, request, pk):
        discussion = self.get_object(pk)
        serializer = DiscussionDetailSerializer(discussion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        discussion = self.get_object(pk)
        serializer = DiscussionCreateUpdateSerializer(discussion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        discussion = self.get_object(pk)
        discussion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
