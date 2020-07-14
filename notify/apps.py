from django.apps import AppConfig


class NotifyConfig(AppConfig):
    name = 'notify'

    def ready(self):
        from . import signals
