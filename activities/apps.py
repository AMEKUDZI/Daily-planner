import logging
import os
import sys

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class ActivitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'activities'

    def ready(self):
        # Only start the background scheduler when actually serving the app,
        # not during makemigrations/migrate/shell/etc.
        if not any('runserver' in arg for arg in sys.argv):
            return
        # Avoid starting it twice under the dev server's autoreloader
        if os.environ.get('RUN_MAIN') != 'true':
            return
        from . import scheduler
        try:
            scheduler.start()
        except Exception:
            logger.exception('Failed to start the activity scheduler')
