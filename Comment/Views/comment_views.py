from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Comment.models import Comment
from Comment.Serializers.comment_serializer import (
    CommentListSerializer,
    CommentDetailSerializer,
    CommentCreateSerializer
)
from django.shortcuts import get_object_or_404


# API for listing and creating comments
class CommentListCreateAPIView(APIView):

    def get(self, request):
        comments = Comment.objects.filter(reply=None)  # Top-level comments only
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API for retrieving, updating, and deleting a specific comment
class CommentDetailAPIView(APIView):

    def get_object(self, pk):
        return get_object_or_404(Comment, pk=pk)

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentDetailSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentCreateSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(CommentDetailSerializer(comment).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
