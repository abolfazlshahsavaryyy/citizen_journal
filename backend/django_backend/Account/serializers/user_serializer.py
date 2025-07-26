from rest_framework import serializers
from Account.models.Profile  import  Profile
from Account.models.ApplicationUser import ApplicationUser
from Page.models import Page


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

        

        return user
