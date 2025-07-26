# serializers.py
from rest_framework import serializers
from Page.models.Page import Page

class FollowSerializer(serializers.Serializer):
    message = serializers.CharField()
    follower_count = serializers.IntegerField()
    following_count = serializers.IntegerField()

class UnfollowSerializer(serializers.Serializer):
    message = serializers.CharField()
    follower_count = serializers.IntegerField()
    following_count = serializers.IntegerField()




class PageSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'name', 'follower_count', 'following_count']
