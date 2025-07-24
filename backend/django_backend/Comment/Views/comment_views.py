from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Comment.models import Comment
from Comment.Serializers.comment_serializer import (
    CommentListSerializer,
    CommentDetailSerializer,
    CommentCreateSerializer,
    CommentUpdateSerializer,
    RecursiveCommentSerializer
)
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from Page.models import News

# API for listing and creating comments
class CommentListCreateAPIView(APIView):

    def get(self, request):
        comments = Comment.objects.filter(reply=None)  # Top-level comments only
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        request_body=CommentCreateSerializer,
        responses={201: CommentCreateSerializer}
    )
    def post(self, request):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
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
    @swagger_auto_schema(
        request_body=CommentUpdateSerializer,
        responses={201: CommentUpdateSerializer}
    )
    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if request.user != comment.user:
            return Response({'detail': 'You are not allowed to update this comment.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CommentUpdateSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            updated_comment = serializer.save()
            return Response(CommentDetailSerializer(updated_comment).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        if(comment.user!=request.user):
            return Response({'detail': 'You are not allowed to update this comment.'},
                            status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentNewsView(APIView):
    def get(self, request, news_pk):
        news = get_object_or_404(News, pk=news_pk)
        
        # Get only top-level comments (not replies)
        top_comments = Comment.objects.filter(news=news, reply__isnull=True)

        serializer = RecursiveCommentSerializer(top_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



