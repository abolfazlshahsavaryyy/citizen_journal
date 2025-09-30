from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView, TokenBlacklistView
from django.urls import path
from Page.graphql.schema import schema
from django.views.decorators.csrf import csrf_exempt
from Page.graphql.view import DRFAwareGraphQLView

schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),  # FIXED HERE
)
admin_url=[path('admin/', admin.site.urls)]

authentication_url=[
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),# it used to verify wether the toekn is correct or not
    path("api/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),# it used to invalidate the refresh toekn
    ]

app_url=[
    path('pages/', include('Page.urls')),
    path('comment/', include('Comment.urls')),
    path('discussion/', include("Discussion.urls")),
    path('question/', include("Question.urls")),
    path('account/', include('Account.urls')),
    path('notification/', include('Notification.urls')),
]
graphql_url=[
  
    path("graphql/", csrf_exempt(DRFAwareGraphQLView.as_view(graphiql=True))),
]
swagger_url=[
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

urlpatterns = admin_url+authentication_url+app_url+graphql_url+swagger_url
