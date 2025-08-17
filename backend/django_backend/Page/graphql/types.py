# app/graphql/types.py
import strawberry
from typing import List
from Page.models.News import News
from datetime import datetime

@strawberry.django.type(News)
class NewsType:
    id: strawberry.ID
    title: str
    text: str
    like_count: int
    comment_count: int
    published_date: datetime
    updated_at: datetime
