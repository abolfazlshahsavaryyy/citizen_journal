from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import NotificationSerializer
from .notification_service import get_user_notifications

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = get_user_notifications(request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
