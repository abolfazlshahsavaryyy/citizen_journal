
from rest_framework import generics, permissions
from Account.serializers.profiie_serializer import ProfileSerializer
from drf_yasg.utils import swagger_auto_schema

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
