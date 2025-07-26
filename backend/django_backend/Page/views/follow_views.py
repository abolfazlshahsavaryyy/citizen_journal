# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from Page.models.Page import Page
from Page.serializer.follow_serializer import *

class FollowPageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, follower_page_id, target_page_id):
        try:
            follower_page = Page.objects.get(id=follower_page_id, user=request.user)
        except Page.DoesNotExist:
            return Response({"detail": "You do not own this follower page."}, status=status.HTTP_403_FORBIDDEN)

        if follower_page_id == target_page_id:
            return Response({"detail": "A page cannot follow itself."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_page = Page.objects.get(id=target_page_id)
        except Page.DoesNotExist:
            return Response({"detail": "Target page does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if target_page in follower_page.follows.all():
            return Response({"detail": "Already following this page."}, status=status.HTTP_400_BAD_REQUEST)

        # Perform the follow
        follower_page.follows.add(target_page)

        # Update counts
        follower_page.following_count += 1
        target_page.follower_count += 1
        follower_page.save()
        target_page.save()

        data = {
            "message": f"{follower_page.name} now follows {target_page.name}.",
            "follower_count": target_page.follower_count,
            "following_count": follower_page.following_count,
        }
        serializer = FollowSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)




class UnfollowPageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, follower_page_id, target_page_id):
        # ✅ Ownership check
        try:
            follower_page = Page.objects.get(id=follower_page_id, user=request.user)
        except Page.DoesNotExist:
            return Response(
                {"detail": "You do not own this page."},
                status=status.HTTP_403_FORBIDDEN
            )

        # ✅ Self-unfollow prevention
        if follower_page_id == target_page_id:
            return Response(
                {"detail": "A page cannot unfollow itself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Target existence check
        try:
            target_page = Page.objects.get(id=target_page_id)
        except Page.DoesNotExist:
            return Response(
                {"detail": "Target page does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ Must already follow
        if target_page not in follower_page.follows.all():
            return Response(
                {"detail": "This page is not currently followed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Remove follow
        follower_page.follows.remove(target_page)

        # ✅ Update counters
        follower_page.following_count = max(0, follower_page.following_count - 1)
        target_page.follower_count = max(0, target_page.follower_count - 1)
        follower_page.save()
        target_page.save()

        data = {
            "message": f"{follower_page.name} has unfollowed {target_page.name}.",
            "follower_count": target_page.follower_count,
            "following_count": follower_page.following_count,
        }

        serializer = UnfollowSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


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
