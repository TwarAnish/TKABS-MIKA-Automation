from django.apps import AppConfig


class CapacityPlanningConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'capacity_planning'

    def ready(self):
        import capacity_planning.signals  # noqa
