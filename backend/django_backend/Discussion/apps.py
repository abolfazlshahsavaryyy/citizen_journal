from django.apps import AppConfig
from pathlib import Path

class DiscussionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Discussion'
    def ready(self):
        from config.interceptor import configure_logging

        project_root = Path(__file__).resolve().parents[2]
        configure_logging(
            log_level="INFO",
            log_dir=str(project_root / "logs"),
            rotation="10 MB",
            retention="30 days",
            compression="zip",
        )
