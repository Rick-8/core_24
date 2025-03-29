from django.apps import AppConfig


class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookings'

    def ready(self):
        # Importing bookings.signals to register signal handlers
        # Importing bookings.signals to ensure signal handlers are registered
        import bookings.signals  # noqa: F401
