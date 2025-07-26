# serializers.py
from rest_framework import serializers
from Page.models.News import News
from django.contrib.auth import get_user_model

User = get_user_model()

class NewsLikeCreateSerializer(serializers.Serializer):
    news_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        # Ensure News and User exist
        try:
            data['news'] = News.objects.get(id=data['news_id'])
        except News.DoesNotExist:
            raise serializers.ValidationError("News post not found.")

        try:
            data['user'] = User.objects.get(id=data['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        return data

    def create(self, validated_data):
        news = validated_data['news']
        user = validated_data['user']
        news.likes.add(user)
        news.like_count = news.likes.count()
        news.save()
        return {'news_id': news.id, 'user_id': user.id}
    
# serializers.py (continue)
class NewsLikeReadSerializer(serializers.Serializer):
    news_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
