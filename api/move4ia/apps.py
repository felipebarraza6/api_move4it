from django.apps import AppConfig


class Move4iaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.move4ia'

    def ready(self):
        import api.move4ia.signals
