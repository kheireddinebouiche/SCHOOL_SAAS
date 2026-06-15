from django.apps import AppConfig


class TStageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 't_stage'

    def ready(self):
        import t_stage.signals
