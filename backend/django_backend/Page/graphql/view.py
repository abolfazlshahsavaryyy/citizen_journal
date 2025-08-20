from graphene_django.views import GraphQLView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class DRFAwareGraphQLView(GraphQLView):
    def parse_body(self, request):
        jwt_auth = JWTAuthentication()
        user_auth_tuple = jwt_auth.authenticate(request)
        if user_auth_tuple is not None:
            request.user, request.auth = user_auth_tuple
        return super().parse_body(request)
