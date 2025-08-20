# config/utils.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

User = get_user_model()

def get_user_from_drf_token(payload):
    try:
        # payload is already decoded if GraphQL-JWT calls us
        user_id = payload.get("user_id")
        if not user_id:
            raise AuthenticationFailed("Invalid payload: no user_id")
        return User.objects.get(id=user_id)
    except Exception:
        raise InvalidToken("Invalid JWT token")
