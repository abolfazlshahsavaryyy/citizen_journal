# serializers.py
from rest_framework import serializers
from Page.models.News import News
from django.contrib.auth import get_user_model

User = get_user_model()

class NewsToggleLikeSerializer(serializers.Serializer):
    news_id = serializers.IntegerField()

    def validate_news_id(self, value):
        try:
            news = News.objects.get(id=value)
        except News.DoesNotExist:
            raise serializers.ValidationError("News not found.")
        return news

    def create(self, validated_data):
        # Not used here because service handles logic
        pass

    
# serializers.py (continue)
class NewsLikeReadSerializer(serializers.Serializer):
    news_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
