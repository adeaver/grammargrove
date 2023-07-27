from django.apps import AppConfig

import logging


class OpsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ops'

    def ready(self):
        try:
            from .featureflags import initialize_feature_flags
            initialize_feature_flags()
            logging.warn("Initialized feature flags")
        except Exception as e:
            logging.warn(e)

