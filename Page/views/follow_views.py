# api that get the Id and show the all pages that this page with that Id has follows
# api that get the Id and show the all page that this page has follwed_by
# api to add new follow and followed_by relation
# api to delete the relation of following
# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from Page.models import Page
from Page.serializer.follow_serializer import *

class FollowListView(APIView):
    def get(self, request):
        """
        
        - GET /api/follows/  → get all follow relationships
        """
        
        
        data = []
        pages = Page.objects.all().prefetch_related('follows')
        for follower in pages:
            for following in follower.follows.all():
                data.append({
                    "follower_id": follower.id,
                    "follower_name": follower.name,
                    "following_id": following.id,
                    "following_name": following.name
                })
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FollowCreateSerializer(data=request.data)
        if serializer.is_valid():
            relation = serializer.save()
            return Response({
                "message": "Follow relationship created successfully.",
                "follower": relation['follower'].name,
                "following": relation['following'].name,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class FollowDetailesView(APIView):

    def get(self, request, pk=None):
        action = request.query_params.get("type")  # expects 'following' or 'followers'

        page = get_object_or_404(Page, pk=pk)

        if action == "following":
            follows = page.follows.all()
            serializer = PageMinimalSerializer(follows, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif action == "followers":
            followers = page.followed_by.all()
            serializer = PageMinimalSerializer(followers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"error": "Please specify 'type' as 'following' or 'followers' in query params."},
            status=status.HTTP_400_BAD_REQUEST
        )

    
    def delete(self, request):
        follower_id = request.data.get("follower_id")
        following_id = request.data.get("following_id")

        if not follower_id or not following_id:
            return Response({"error": "Both follower_id and following_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        follower = get_object_or_404(Page, pk=follower_id)
        following = get_object_or_404(Page, pk=following_id)

        if following in follower.follows.all():
            follower.follows.remove(following)
            # Optionally update counters
            follower.following_count -= 1
            following.follower_count -= 1
            follower.save()
            following.save()
            return Response({"message": "Unfollowed successfully."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "This follow relationship does not exist."}, status=status.HTTP_400_BAD_REQUEST)
