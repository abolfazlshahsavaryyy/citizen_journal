import graphene
from graphene_django.types import DjangoObjectType
from Page.models.News import News
import graphql_jwt

class NewsType(DjangoObjectType):
    class Meta:
        model = News


class Query(graphene.ObjectType):
    all_news = graphene.List(NewsType)

    def resolve_all_news(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")
        return News.objects.all()

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

