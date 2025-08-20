from django.middleware.common import CommonMiddleware
from loguru import logger

class CustomCommonMiddleware:
    def __init__(self, get_response):
        self.base_middleware = CommonMiddleware(get_response)

    def __call__(self, request):
        logger.debug("[CustomCommonMiddleware] Processing common request: {}", request.path)
        return self.base_middleware(request)
