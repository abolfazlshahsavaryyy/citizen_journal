from rest_framework import serializers
from Question.models.question import Question
from Discussion.models import Topic

class TopicMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title']


class QuestionSerializer(serializers.ModelSerializer):
    topic = TopicMiniSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ['content', 'created_at', 'is_private', 'topic']



class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class QuestionDetailSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'content', 'created_at', 'is_private', 'topic']

class QuestionCreateSerializer(serializers.ModelSerializer):
    topic_id = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(),
        source='topic',
        write_only=True
    )

    class Meta:
        model = Question
        fields = ['content', 'is_private', 'topic_id']

class QuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['content', 'is_private']
