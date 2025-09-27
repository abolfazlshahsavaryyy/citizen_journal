from rest_framework import serializers
from django.contrib.auth import get_user_model
from Page.models.News import News
User = get_user_model()
# For GET response
class ShareNewsMessageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    userIdSender = serializers.IntegerField()
    newsId = serializers.IntegerField()
    userIdReceiver = serializers.IntegerField()
    content = serializers.CharField()
    createdAt = serializers.CharField()  # gRPC uses string

class GetShareNewsByUserResponseSerializer(serializers.Serializer):
    items = ShareNewsMessageSerializer(many=True)


# For AddShareNews
class AddShareNewsRequestSerializer(serializers.Serializer):
    newsId = serializers.IntegerField()
    userIdReceiver = serializers.IntegerField()
    content = serializers.CharField(required=False, allow_blank=True)

    def validate_userIdReceiver(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Receiver user does not exist.")
        return value

    def validate_newsId(self, value):
        if not News.objects.filter(id=value).exists():
            raise serializers.ValidationError("News does not exist.")
        return value

class AddShareNewsResponseSerializer(serializers.Serializer):
    item = ShareNewsMessageSerializer()


# For RemoveShareNews
class RemoveShareNewsRequestSerializer(serializers.Serializer):
    shareNewsId = serializers.IntegerField()

class RemoveShareNewsResponseSerializer(serializers.Serializer):
    shareNewsId = serializers.IntegerField()
