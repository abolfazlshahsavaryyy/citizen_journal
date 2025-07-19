from rest_framework import serializers
from Discussion.models import Topic, Discussion


class TopicListSerializer(serializers.ModelSerializer):
    discussion_name = serializers.CharField(source='discussion.name', read_only=True)

    class Meta:
        model = Topic
        fields = [
            'id', 'title', 'description',
            'created_at', 'updated_at',
            'discussion', 'discussion_name'
        ]


class TopicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['discussion', 'title', 'description']

class TopicUpdateSerializer(serializers.ModelSerializer):
    discussion = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Topic
        fields = ['discussion', 'title', 'description']



class DiscussionBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = ['id', 'name', 'description', 'is_active']


class TopicDetailSerializer(serializers.ModelSerializer):
    discussion = DiscussionBasicSerializer(read_only=True)

    class Meta:
        model = Topic
        fields = [
            'id', 'title', 'description',
            'created_at', 'updated_at',
            'discussion'
        ]
