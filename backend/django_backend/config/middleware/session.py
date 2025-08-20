# config/middleware/session.py
from django.contrib.sessions.middleware import SessionMiddleware
from loguru import logger

class CustomSessionMiddleware(SessionMiddleware):
    def __init__(self, get_response):
        super().__init__(get_response)

    def __call__(self, request):
        logger.debug("[CustomSessionMiddleware] Managing session for {}", request.path)
        return super().__call__(request)
