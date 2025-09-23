from django.test import TestCase

# Create your tests here.
import redis
import requests
from celery import shared_task
from django.apps import apps
from loguru import logger
# Redis client
redis_client = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

FASTAPI_URL = "http://summarizer:8003/summarize"

@shared_task
def summarize_news_task(news_id,text):
    

    # Call FastAPI summarizer
    response = requests.post(FASTAPI_URL, json={"text": text})
    logger.info('send the request to summarizer api endpoint')
    summary = response.json().get("summary")

    # Save in Redis
    logger.info(f'set the news:{news_id}:summary as key and value is summary of this news text ')
    redis_client.set(f"news:{news_id}:summary", summary)

    return summary
