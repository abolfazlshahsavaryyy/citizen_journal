from rest_framework import serializers
from Account.models.Profile import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'bio', 'avatar', 'created_at', 'updated_at', 'reputation', 'last_activity']