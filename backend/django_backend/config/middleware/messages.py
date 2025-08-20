from django.contrib.messages.middleware import MessageMiddleware
from loguru import logger

class CustomMessageMiddleware(MessageMiddleware):
    def __init__(self, get_response):
        super().__init__(get_response)

    def __call__(self, request):
        logger.debug("[CustomMessageMiddleware] Handling messages for {}", request.path)
        return super().__call__(request)
