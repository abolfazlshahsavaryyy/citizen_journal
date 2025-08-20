from corsheaders.middleware import CorsMiddleware
from loguru import logger

class CustomCorsMiddleware:
    def __init__(self, get_response):
        self.base_middleware = CorsMiddleware(get_response)

    def __call__(self, request):
        logger.debug("[CustomCorsMiddleware] Handling CORS for {}", request.path)
        return self.base_middleware(request)
