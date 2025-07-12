# accounts/serializers.py

from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'bio', 'avatar', 'created_at', 'updated_at', 'reputation', 'last_activity']

# Account/serializers.py
from rest_framework import serializers
from Account.models import ApplicationUser, Profile
from Page.models import Page
from Discussion.models import Discussion

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ApplicationUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = ApplicationUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='citizen'  # Always citizen
        )

        # Create Profile
        Profile.objects.create(user=user)

        # Create Page
        page = Page.objects.create(
            name=f"{user.username}_page",
            user=user,
            page_description=f"{user.username}'s default page"
        )

        # Create Discussion
        Discussion.objects.create(
            name=f"{user.username}'s discussion",
            description="Auto-created discussion for user page",
            page=page
        )

        return user
