from django.apps import AppConfig


class TCrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 't_crm'

    def ready(self):
        import t_crm.signals
