from rest_framework import serializers
from Page.models.Page import Page
from Page.models.News import News
from django.contrib.auth import get_user_model

#this class is not for here 
#it has to be in vserializer/news_serializer
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
# Account/serializers.py
class MiniUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']


class PageSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(read_only=True)

    class Meta:
        model = Page
        fields = [
            'id',
            'name',
            'post_count',
            'follower_count',
            'following_count',
            'page_description',
            'created_at',
            'updated_at',
            'user',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['name', 'page_description']

    def create(self, validated_data):
        # Add default values here before saving
        validated_data['post_count'] = 0
        validated_data['follower_count'] = 0
        validated_data['following_count'] = 0
        # Now create the instance with those values
        return Page.objects.create(**validated_data)
    

class PageDetailseSerializer(serializers.ModelSerializer):
    news_posts = NewsSerializer(many=True, read_only=True)
    user=MiniUserSerializer(read_only=True)
    # Follows relationship - show by name or ID (choose one)
    follows = serializers.SlugRelatedField(
        slug_field='id',  # or 'id' for PrimaryKeyRelatedField
        queryset=Page.objects.all(),
        many=True,
        required=False
    )
    class Meta:
        model=Page
        fields='__all__'

class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Page
        fields=['name','page_description']
        
    