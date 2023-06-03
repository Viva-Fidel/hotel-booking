from django.apps import AppConfig


class HotelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotels'
    verbose_name = "Hotel managment"

    def ready(self):
        import hotels.signals
