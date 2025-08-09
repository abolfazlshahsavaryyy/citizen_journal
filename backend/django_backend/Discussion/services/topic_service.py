# services/topic_service.py
from rest_framework.exceptions import PermissionDenied, NotFound
from Discussion.models.Discussion import Discussion
from Discussion.models.Topic import Topic

class TopicService:
    @staticmethod
    def create_topic(validated_data, user):
        discussion = validated_data['discussion']

        # Check discussion exists with related page
        try:
            discussion = Discussion.objects.select_related('page').get(id=discussion.id)
        except Discussion.DoesNotExist:
            raise NotFound('Discussion not found.')

        # Permission check
        if discussion.page.user != user:
            raise PermissionDenied('You do not have permission to add a topic to this discussion.')

        # Create topic
        topic = Topic.objects.create(**validated_data)
        return topic
    @staticmethod
    def update_topic(topic, validated_data, user):
        # Permission check
        if topic.discussion.page.user != user:
            raise PermissionDenied('You do not have permission to update this topic.')

        # Update topic
        for attr, value in validated_data.items():
            setattr(topic, attr, value)
        topic.save()

        return topic

    @staticmethod
    def delete_topic(topic, user):
        # Permission check
        if topic.discussion.page.user != user:
            raise PermissionDenied('You do not have permission to delete this topic.')

        topic.delete()

