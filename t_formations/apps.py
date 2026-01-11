from django.apps import AppConfig


class TFormationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 't_formations'

    def ready(self):
        import t_formations.signals
