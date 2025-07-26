from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from Discussion.models.Discussion import Discussion
from Discussion.Serializers.discussion_serializer import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from Page.models import Page

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
        discussion = self.get_object(pk)

        # 🔒 Permission check: Is the current user the owner of the page?
        if discussion.page.user != request.user:
            return Response({'detail': 'You do not have permission to edit this discussion.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = DiscussionUpdateSerializer(discussion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        discussion = self.get_object(pk)
        if(discussion.page.user!=request.user):
            return Response({'detail': 'You do not have permission to delete this discussion.'},
                            status=status.HTTP_403_FORBIDDEN)
        discussion.delete()
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
        # 1. User must be authenticated (enforced by permission_classes)
        user = request.user
        # 2. Get the Page by pk
        page = get_object_or_404(Page, pk=page_pk)
        # 3. Check if the Page already has a Discussion
        if hasattr(page, 'discussion'):
            return Response({'detail': 'This Page already has a Discussion configured.'}, status=status.HTTP_400_BAD_REQUEST)
        # 4. Check if the Page belongs to the user
        if page.user != user:
            return Response({'detail': 'You do not have permission to create a Discussion for this Page.'}, status=status.HTTP_403_FORBIDDEN)
        # 5. Create the Discussion
        data = request.data.copy()
        data['page'] = page.pk
        serializer = DiscussionCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
