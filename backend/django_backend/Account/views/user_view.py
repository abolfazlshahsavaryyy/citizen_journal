# Account/views/register_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Account.serializers.user_serializer import RegisterSerializer
from Account.services.user_service import register_user
from drf_yasg.utils import swagger_auto_schema
from loguru import logger as log

class RegisterView(APIView):
    authentication_classes = []  # No auth needed
    permission_classes = []      # Public access

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: "User created successfully"}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = register_user(
                username=serializer.validated_data["username"],
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"]
            )
            log.success(f'user with username {user.username} created succesfully')
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
