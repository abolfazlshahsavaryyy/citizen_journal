# serializers.py
from rest_framework import serializers
from Page.models.Page import Page

# serializers/follow_toggle_serializer.py
from rest_framework import serializers

class FollowToggleInputSerializer(serializers.Serializer):
    follower_page_id = serializers.IntegerField()
    target_page_id = serializers.IntegerField()

    
class FollowToggleOutputSerializer(serializers.Serializer):
    message = serializers.CharField()
    follower_count = serializers.IntegerField()
    following_count = serializers.IntegerField()
    action = serializers.CharField()  # "followed" or "unfollowed"




class PageSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'name', 'follower_count', 'following_count']
