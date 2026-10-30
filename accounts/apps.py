from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals
