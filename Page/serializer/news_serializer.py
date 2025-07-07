# serializers.py
from rest_framework import serializers
from Page.models import News
from Page.models import Page

class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'text', 'page']  # Only required on creation

    def create(self, validated_data):
        page = validated_data.get('page')

        if not page:
            raise serializers.ValidationError("Page is required.")

        # Increment post count
        page.post_count += 1
        page.save()

        # Create the news post
        news = News.objects.create(**validated_data)
        return news

class NewsReadSerializer(serializers.ModelSerializer):
    page_name = serializers.CharField(source='page.name', read_only=True)
    page_follower=serializers.IntegerField(source='page.follower_count', read_only=True)
    class Meta:
        model = News
        fields = [
            'id', 'title', 'text',
            'like_count', 'page', 'page_name','page_follower',
            'published_date', 'updated_at'
        ]
