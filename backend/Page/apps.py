from django.apps import AppConfig


class PageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Page'
    def ready(self):
        import Page.signals

