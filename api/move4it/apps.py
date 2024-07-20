from django.apps import AppConfig


class Move4itConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.move4it'

    def ready(self):
        import api.move4it.signals
