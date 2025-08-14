# core/middleware/request_logging.py
import time
import uuid
from typing import Optional
from django.http import HttpRequest, HttpResponse, StreamingHttpResponse
from loguru import logger

SKIP_PATHS = ("/health", "/ready", "/metrics", "/static/", "/favicon.ico")

def _client_ip(request: HttpRequest) -> str:
    # Be mindful of proxies; configure your trusted proxy headers properly.
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "-")

def _content_length(response: HttpResponse) -> Optional[int]:
    # Avoid forcing evaluation of streaming responses
    if isinstance(response, StreamingHttpResponse):
        return response.get("Content-Length")
    try:
        return len(response.content)
    except Exception:
        return response.get("Content-Length")

class RequestLoggingMiddleware:
    """
    Logs every request/response with timing, status, path, method, user, ip and a request_id.
    Uses Loguru's contextualize() so request_id appears on all lines within the request scope.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        path = request.get_full_path()
        # Optional: skip very noisy endpoints
        if path.startswith(SKIP_PATHS):
            return self.get_response(request)

        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        ip = _client_ip(request)
        method = request.method
        ua = request.META.get("HTTP_USER_AGENT", "-")

        start = time.monotonic()

        # Bind request_id so it shows in all log lines during this context
        with logger.contextualize(request_id=request_id):
            logger.info(
                "REQUEST start | {method} {path} | ip={ip} ua={ua}",
                method=method, path=path, ip=ip, ua=ua,
            )

            try:
                response = self.get_response(request)
            except Exception:
                duration_ms = (time.monotonic() - start) * 1000
                logger.exception(
                    "REQUEST error | {method} {path} | duration_ms={duration_ms:.2f}",
                    method=method, path=path, duration_ms=duration_ms,
                )
                raise

            duration_ms = (time.monotonic() - start) * 1000

            # request.user is available only after AuthenticationMiddleware
            user_label = "anonymous"
            user = getattr(request, "user", None)
            if getattr(user, "is_authenticated", False):
                user_label = getattr(user, "username", "user")

            length = _content_length(response)
            status = getattr(response, "status_code", "-")

            logger.info(
                "RESPONSE end   | {status} {method} {path} | user={user} "
                "duration_ms={duration_ms:.2f} bytes={length}",
                status=status, method=method, path=path,
                user=user_label, duration_ms=duration_ms, length=length,
            )

            # echo request id back to client for tracing
            response["X-Request-ID"] = request_id
            return response
