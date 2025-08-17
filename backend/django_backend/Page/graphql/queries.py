# app/graphql/queries.py
import strawberry
from typing import List
from Page.graphql.types import NewsType
from Page.models.News import News

@strawberry.type
class Query:
    @strawberry.field
    def all_news(self) -> List[NewsType]:
        # Return all news posts, ordered by published_date (from your model's Meta)
        return News.objects.all()
