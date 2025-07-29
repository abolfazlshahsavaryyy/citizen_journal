from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from Discussion.models.Topic import Topic
from Discussion.Serializers.topic_serializer import *
from Discussion.services.topic_service import *
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
    @swagger_auto_schema(
        request_body=TopicCreateSerializer,
        responses={201: TopicCreateSerializer}
    )
    def post(self, request):
        serializer = TopicCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                topic = TopicService.create_topic(serializer.validated_data, request.user)
            except Exception as e:
                
                raise e  
            
            response_serializer = TopicCreateSerializer(topic)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

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
    @swagger_auto_schema(
        request_body=TopicUpdateSerializer,
        responses={201: TopicUpdateSerializer}
    )
    def put(self, request, pk):
        topic = self.get_object(pk)
        serializer = TopicUpdateSerializer(topic, data=request.data)
        if serializer.is_valid():
            try:
                updated_topic = TopicService.update_topic(topic, serializer.validated_data, request.user)
            except Exception as e:
                raise e  # DRF will convert PermissionDenied/NotFound automatically

            response_serializer = TopicUpdateSerializer(updated_topic)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        topic = self.get_object(pk)
        topic_title=topic.title
        id_topic=pk
        try:
            TopicService.delete_topic(topic, request.user)
        except Exception as e:
            raise e  # DRF handles PermissionDenied

        return Response(data={'id':id_topic,'message':f'the topic with title {topic_title} has been deleted'},status=status.HTTP_204_NO_CONTENT)


class GetTopicOfDiscussion(APIView):
    """
    Get all Topics for a specific Discussion.
    """
    def get(self, request, discussion_id):
        # 1. Check if discussion exists
        discussion = get_object_or_404(Discussion, id=discussion_id)
        
        # 2. Get all topics related to that discussion
        topics = Topic.objects.filter(discussion=discussion)
        
        # 3. Serialize and return
        serializer = TopicDetailSerializer(topics, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    


