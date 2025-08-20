from loguru import logger
class DebugMiddleware:
    def resolve(self, next, root, info, **kwargs):
        print("AUTH HEADER:", info.context.META.get("HTTP_AUTHORIZATION"))
        logger.info('this is the header:')
        logger.info("AUTH HEADER:", info.context.META.get("HTTP_AUTHORIZATION"))
        return next(root, info, **kwargs)

