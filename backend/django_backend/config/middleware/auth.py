from django.contrib.auth.middleware import AuthenticationMiddleware
from loguru import logger

class CustomAuthMiddleware(AuthenticationMiddleware):
    def __init__(self, get_response):
        super().__init__(get_response)

    def __call__(self, request):
        logger.info("[CustomAuthMiddleware] Authenticating user for {}", request.path)
        return super().__call__(request)
