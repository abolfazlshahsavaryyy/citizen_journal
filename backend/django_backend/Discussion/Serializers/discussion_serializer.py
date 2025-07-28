from rest_framework import serializers
from Discussion.models.Discussion import Discussion
from Discussion.models.Topic import Topic


class DiscussionListSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = Discussion
        fields = ['id', 'name', 'short_description', 'is_active', 'created_at']

    def get_short_description(self, obj):
        return obj.description[:100]  # Return first 100 characters


class TopicTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['title']


class DiscussionDetailSerializer(serializers.ModelSerializer):
    topics = TopicTitleSerializer(many=True, read_only=True)

    class Meta:
        model = Discussion
        fields = [
            'id', 'name', 'description', 'is_active',
            'created_at', 'updated_at', 'topics'
        ]


class DiscussionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = ['name', 'description', 'is_active']


class DiscussionCreateSerializer(serializers.ModelSerializer):
    page = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Discussion
        fields = ['name', 'description', 'is_active', 'page']

