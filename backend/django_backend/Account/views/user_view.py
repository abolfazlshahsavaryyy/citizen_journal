

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Account.serializers.user_serializer import RegisterSerializer
from drf_yasg.utils import swagger_auto_schema

class RegisterView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []      # Allow any user to register
    
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: RegisterSerializer}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
