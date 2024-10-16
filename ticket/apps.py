from django.apps import AppConfig


class TicketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ticket'

    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()