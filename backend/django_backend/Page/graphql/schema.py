# app/graphql/schema.py
import strawberry
from Page.graphql.queries import Query

schema = strawberry.Schema(query=Query)
