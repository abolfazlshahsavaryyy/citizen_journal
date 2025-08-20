import graphene
from graphene_django.types import DjangoObjectType
from Page.models.News import News
import graphql_jwt
from django.contrib.auth import get_user_model


class NewsType(DjangoObjectType):
    class Meta:
        model = News


class Query(graphene.ObjectType):
    all_news = graphene.List(NewsType)
    recommended_news = graphene.List(NewsType)

    def resolve_all_news(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")
        return News.objects.all()

    def resolve_recommended_news(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")

        # 1. News that current user likes
        user_liked_news = News.objects.filter(likes=user)

        # 2. Other users who liked those news
        similar_users = (
            get_user_model()
            .objects.filter(liked_news__in=user_liked_news)
            .exclude(id=user.id)
            .distinct()
        )

        # 3. News those users like
        recommended_news = (
            News.objects.filter(likes__in=similar_users)
            .exclude(likes=user)  # remove ones user already likes
            .distinct()
        )

        return recommended_news

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

