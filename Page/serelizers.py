from rest_framework import serializers
from .models import Page, News


class NewsSerializer(serializers.ModelSerializer):
    # Optionally include page name or ID
    page = serializers.SlugRelatedField(
        slug_field='id',  # use 'id' if you prefer raw IDs
        queryset=Page.objects.all()
    )

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'text',
            'like_count',
            'page',
            'published_date',
            'updated_at',
        ]
        read_only_fields = ['id', 'published_date', 'updated_at']


class PageSerializer(serializers.ModelSerializer):
    # Nested news posts (read-only for display)
    news_posts = NewsSerializer(many=True, read_only=True)

    # Follows relationship - show by name or ID (choose one)
    follows = serializers.SlugRelatedField(
        slug_field='id',  # or 'id' for PrimaryKeyRelatedField
        queryset=Page.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Page
        fields = [
            'id',
            'name',
            'post_count',
            'follower_count',
            'following_count',
            'page_description',
            'follows',
            'created_at',
            'updated_at',
            'news_posts',  # shows related news
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
