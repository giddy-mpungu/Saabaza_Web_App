import os

from django.conf import settings

from .runtime import celery_class

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appsaabaza.settings.production')

app = celery_class('appsaabaza')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
