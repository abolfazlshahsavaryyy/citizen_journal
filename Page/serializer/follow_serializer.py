
# serializers.py

from rest_framework import serializers
from Page.models import Page

class PageMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'name']

class FollowCreateSerializer(serializers.Serializer):
    follower_id = serializers.IntegerField()
    following_id = serializers.IntegerField()

    def validate(self, data):
        if data['follower_id'] == data['following_id']:
            raise serializers.ValidationError("A page cannot follow itself.")
        return data

    def create(self, validated_data):
        follower = Page.objects.get(pk=validated_data['follower_id'])
        following = Page.objects.get(pk=validated_data['following_id'])

        follower.follows.add(following)
        # Optionally update counters
        follower.following_count += 1
        following.follower_count += 1
        follower.save()
        following.save()

        return {
            'follower': follower,
            'following': following
        }
