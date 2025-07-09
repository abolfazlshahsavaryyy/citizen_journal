from rest_framework import serializers
from Question.models.answer import Answer
from Question.models.question import Question

class QuestionShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'content']


class AnswerListSerializer(serializers.ModelSerializer):
    question = QuestionShortSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'content', 'created_at', 'updated_at', 'question']
class QuestionFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerDetailSerializer(serializers.ModelSerializer):
    question = QuestionFullSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
class AnswerCreateSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(),
        source='question',
        write_only=True
    )

    class Meta:
        model = Answer
        fields = ['content', 'question_id']
class AnswerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['content']
