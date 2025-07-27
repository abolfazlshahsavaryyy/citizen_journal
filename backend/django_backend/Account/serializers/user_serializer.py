# Account/serializers/user_serializer.py

from rest_framework import serializers
from Account.models.ApplicationUser import ApplicationUser


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if ApplicationUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def validate_email(self, value):
        if ApplicationUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value
