from django.middleware.clickjacking import XFrameOptionsMiddleware
from loguru import logger

class CustomClickjackingMiddleware:
    def __init__(self, get_response):
        self.base_middleware = XFrameOptionsMiddleware(get_response)

    def __call__(self, request):
        logger.debug("[CustomClickjackingMiddleware] Applying X-Frame-Options for {}", request.path)
        return self.base_middleware(request)
