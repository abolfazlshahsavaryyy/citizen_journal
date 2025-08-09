# services/news_service.py
from django.db import transaction
from Page.models.News import News

class NewsService:
    @staticmethod
    @transaction.atomic
    def create_news(validated_data):
        page = validated_data['page']

        # Increment post count
        page.post_count += 1
        page.save()

        # Create the news post
        return News.objects.create(**validated_data)
    
    @staticmethod
    @transaction.atomic
    def update_news(news, validated_data):
        # Only update fields passed in validated_data (title/text)
        for attr, value in validated_data.items():
            setattr(news, attr, value)
        news.save()
        return news
    
    @staticmethod
    @transaction.atomic
    def delete_news(news):
        """
        Deletes a news post and decrements the related page's post_count.
        """
        page = news.page
        if page.post_count > 0:
            page.post_count -= 1
            page.save()
        news.delete()

