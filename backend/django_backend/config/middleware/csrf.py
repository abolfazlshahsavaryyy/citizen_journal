from django.middleware.csrf import CsrfViewMiddleware
from loguru import logger

class CustomCsrfMiddleware:
    def __init__(self, get_response):
        self.base_middleware = CsrfViewMiddleware(get_response)

    def __call__(self, request):
        logger.debug("[CustomCsrfMiddleware] Checking CSRF for {}", request.path)
        return self.base_middleware(request)
