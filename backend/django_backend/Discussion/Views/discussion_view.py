from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from Discussion.models.Discussion import Discussion
from Discussion.Serializers.discussion_serializer import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from Page.models.Page import Page
from Discussion.services.discussion_service import *
from loguru import logger as log
class DiscussionListCreateView(APIView):
    """
    Handles GET (list all discussions) and POST (create new discussion)
    """

    def get(self, request):
        discussions = Discussion.objects.all()
        serializer = DiscussionListSerializer(discussions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #add the api endpoint to add new Discussion for deleted discussion 

    
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
    @swagger_auto_schema(
        request_body=DiscussionUpdateSerializer,
        responses={201: DiscussionUpdateSerializer}
    )
    def put(self, request, pk):
        serializer = DiscussionUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            updated_discussion = update_discussion(
                user=request.user,
                discussion_id=pk,
                data=serializer.validated_data
            )
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)

        log.success(f'discussion with Id {pk} has been updated')
        return Response(
            
            DiscussionUpdateSerializer(updated_discussion).data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        try:
            delete_discussion(user=request.user, discussion_id=pk)
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        log.info(f'discussion with id {pk} has been deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class DiscussionCreateForPageView(APIView):
    """
    API endpoint to create a new Discussion for a Page, only if:
    - The user is authenticated
    - The Page does not already have a Discussion
    - The Page belongs to the requesting user
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=DiscussionCreateSerializer,
        responses={201: DiscussionCreateSerializer, 400: 'Bad Request', 403: 'Forbidden'}
    )
    def post(self, request, page_pk):
        serializer = DiscussionCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            discussion = create_discussion(
                user=request.user,
                page_id=page_pk,
                data=serializer.validated_data
            )
        except PermissionDenied as e:
            log.error(e[0:100])
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            log.error(e[0:100])
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        log.info(f'dicussion created for page with id {page_pk}')
        return Response(DiscussionCreateSerializer(discussion).data, status=status.HTTP_201_CREATED)


    
class UserDiscussionListView(APIView):
    def get(self, request):
        discussions = DiscussionService.get_user_discussions(request.user)
        serializer = DiscussionSerializer(discussions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)