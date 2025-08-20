from loguru import logger

class FirstAuthRequestMiddleware:
    seen_first_auth = False  # shared across all requests

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info("🚀 Middleware called for path: {}", request.path)

        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header and not FirstAuthRequestMiddleware.seen_first_auth:
            FirstAuthRequestMiddleware.seen_first_auth = False
            logger.info("🔥 First request with Authorization header received: {}", auth_header)

        return self.get_response(request)
