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
from Page.models.News import News
from Comment.services.comment_service import *
# API for listing and creating comments

#import logging
from uuid import uuid4
from loguru import logger as log
import logging

#std_logger = logging.getLogger("django.request")  # example stdlib logger

class CommentListCreateAPIView(APIView):

    def get(self, request):
        comments = Comment.objects.filter(reply=None)  # Top-level comments only
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        request_body=CommentCreateSerializer,
        responses={200: CommentCreateSerializer}
    )
    def post(self, request):
        


        serializer = CommentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Call service
        try:
            comment = create_comment(
            user=request.user,
            content=serializer.validated_data['content'],
            news=serializer.validated_data['news'],
            reply=serializer.validated_data.get('reply')
            )
            log.info('comment added to db')
        except ValidationError as e:
            log.error(e)
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        
        # Return serialized response
        response_serializer = CommentCreateSerializer(comment)
        log.success('comment created successfully')
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)



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
        # Validate input
        serializer = CommentUpdateSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            updated_comment = update_comment(
                user=request.user,
                comment_id=pk,
                data=serializer.validated_data
            )
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)

        return Response(
            CommentDetailSerializer(updated_comment).data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        try:
            delete_comment(user=request.user, comment_id=pk)
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentNewsView(APIView):
    def get(self, request, news_pk):
        news = get_object_or_404(News, pk=news_pk)
        
        # Get only top-level comments (not replies)
        top_comments = Comment.objects.filter(news=news, reply__isnull=True)

        serializer = RecursiveCommentSerializer(top_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



