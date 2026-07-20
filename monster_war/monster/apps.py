from django.apps import AppConfig


class MonsterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'monster'

    def ready(self):
        import monster.signals
