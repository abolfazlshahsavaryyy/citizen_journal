# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from Page.models.Page import Page
from Page.serializer.follow_serializer import *

# views/follow_toggle_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from Page.services.follow_service import toggle_follow
from Page.serializer.follow_serializer import (
    FollowToggleInputSerializer,
    FollowToggleOutputSerializer,
)

class ToggleFollowPageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        request_body=FollowToggleInputSerializer,
        responses={200: FollowToggleInputSerializer}
    )
    def post(self, request):
        # Step 1: Validate input
        input_serializer = FollowToggleInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        follower_page_id = input_serializer.validated_data["follower_page_id"]
        target_page_id = input_serializer.validated_data["target_page_id"]

        # Step 2: Call service
        try:
            action, message, follower_page, target_page = toggle_follow(
                follower_page_id, target_page_id, request.user
            )
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Step 3: Prepare response
        output_data = {
            "message": message,
            "follower_count": target_page.follower_count,
            "following_count": follower_page.following_count,
            "action": action,
        }

        output_serializer = FollowToggleOutputSerializer(output_data)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

class PageFollowersView(APIView):
    def get(self, request, page_id):
        try:
            page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return Response({"detail": "Page not found."}, status=status.HTTP_404_NOT_FOUND)

        followers = page.followed_by.all()
        serializer = PageSummarySerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PageFollowingView(APIView):
    def get(self, request, page_id):
        try:
            page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return Response({"detail": "Page not found."}, status=status.HTTP_404_NOT_FOUND)

        following = page.follows.all()
        serializer = PageSummarySerializer(following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
