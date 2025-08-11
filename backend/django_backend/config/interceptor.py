# myproject/loguru_interceptor.py
import os
import sys
import inspect
import logging
from typing import Optional
from loguru import logger

# guard so repeated imports / Django dev autoreload don't add duplicate handlers
_configured = False

def configure_logging(
    *,
    log_level: str = "INFO",
    log_dir: Optional[str] = None,
    rotation: str = "10 MB",
    retention: str = "14 days",
    compression: Optional[str] = "zip",
    console: bool = True,
    backtrace: bool = True,
    diagnose: bool = False,
):
    """
    Idempotent Loguru + interception setup.

    - log_level: default sink minimum level (e.g. "DEBUG","INFO","ERROR")
    - log_dir: directory for file logs. If None, file sink is not added.
    - rotation: rotation policy (size like "10 MB", time like "00:00", or callable). See Loguru docs.
    - retention: retention policy (e.g. "7 days", or number of files). See Loguru docs.
    - compression: "zip", "gz", etc. or None.
    """
    global _configured
    if _configured:
        return
    _configured = True

    # clear default handlers
    logger.remove()

    # Console sink (nice format)
    if console:
        logger.add(
            sys.stderr,
            level=log_level,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "{name}:{function}:{line} - {message}"
            ),
            colorize=True,
        )

    # File sink with rotation/retention/compression
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        logger.add(
            os.path.join(log_dir, "app_{time:YYYY-MM-DD}.log"),
            level="DEBUG",
            rotation=rotation,
            retention=retention,
            compression=compression,
            backtrace=backtrace,
            diagnose=diagnose,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} - {message}",
        )

    # ---- Intercept stdlib logging -> Loguru ----
    class InterceptHandler(logging.Handler):
        """
        Handler that redirects stdlib logging records to Loguru.
        This is the recipe from Loguru docs adapted for Django.
        """
        def emit(self, record: logging.LogRecord) -> None:
            # Map stdlib level name to Loguru level (fallback to numeric level)
            try:
                level = logger.level(record.levelname).name
            except Exception:
                level = record.levelno

            # Find caller frame depth so Loguru prints correct origin
            frame = inspect.currentframe()
            depth = 2
            # Walk up until leaving logging module frames
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            # Re-log with Loguru
            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    # Replace root handlers so third-party libraries using stdlib logging are intercepted
    # logging.root.handlers = [InterceptHandler()]
    # logging.root.setLevel(logging.DEBUG)

    
