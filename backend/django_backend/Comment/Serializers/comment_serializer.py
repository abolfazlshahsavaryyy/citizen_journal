from rest_framework import serializers
from Comment.models import Comment


# Minimal Serializer for listing comments (GET all)
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'news', 'content', 'created_at']


# Detailed Serializer for retrieving a single comment by ID (GET by id)
class CommentDetailSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'reply', 'news',
            'created_at', 'updated_at', 'replies'
        ]

    def get_replies(self, obj):
        replies = obj.replies.all()
        return CommentDetailSerializer(replies, many=True).data


# Serializer for creating comments
class CommentCreateSerializer(serializers.ModelSerializer):
    reply = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Comment
        fields = ['content', 'news', 'reply']


class CommentUpdateSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Comment
        fields = ['content']


class RecursiveCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'replies']

    def get_replies(self, obj):
        children = obj.replies.all()
        return RecursiveCommentSerializer(children, many=True).data

