# serializers.py
from rest_framework import serializers
from Page.models.News import News
from Page.models.Page import Page

# serializers/news_serializers.py
class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'text', 'page']  # Only required on creation


class NewsReadSerializer(serializers.ModelSerializer):
    page_name = serializers.CharField(source='page.name', read_only=True)
    page_follower=serializers.IntegerField(source='page.follower_count', read_only=True)
    class Meta:
        model = News
        fields = [
            'id', 'title', 'text',
            'like_count','comment_count', 'page', 'page_name','page_follower',
            'published_date', 'updated_at'
        ]

# serializers/news_serializers.py
class NewsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'text']  # Page cannot be updated
