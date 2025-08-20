from django.middleware.security import SecurityMiddleware
from loguru import logger

class CustomSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.base_middleware = SecurityMiddleware(get_response)

    def __call__(self, request):
        logger.info("[CustomSecurityMiddleware] Incoming request: {}", request.path)

        response = self.base_middleware(request)

        logger.info("[CustomSecurityMiddleware] Outgoing response: {}", response.status_code)
        return response
